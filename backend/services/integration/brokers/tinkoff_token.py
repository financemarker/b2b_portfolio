from tinkoff.invest import Client, GetOperationsByCursorRequest, OperationType, InstrumentRequest, InstrumentIdType
from tinkoff.invest.constants import INVEST_GRPC_API
from decimal import Decimal
from typing import Optional, List
from decimal import Decimal
from typing import Optional
from tinkoff.invest import MoneyValue, Quotation, OperationType
from sqlalchemy.orm import Session
from backend.services.integration.brokers.base import BrokerBase, AccountDict
from backend.models.connection import ConnectionStatus
from backend.models import Operation, Instrument, Exchange
from backend.models.instrument import InstrumentCategory, InstrumentStatus
from backend.core import utils


# Mapping from Tinkoff OperationType to our universal operation types
TINKOFF_OPERATION_TYPE_MAPPING = {
    # Trading operations
    OperationType.OPERATION_TYPE_BUY: "buy",
    OperationType.OPERATION_TYPE_SELL: "sell",

    # Income operations
    OperationType.OPERATION_TYPE_DIVIDEND: "dividend",
    OperationType.OPERATION_TYPE_COUPON: "coupon",

    # Fees and taxes
    OperationType.OPERATION_TYPE_BROKER_FEE: "commission",
    OperationType.OPERATION_TYPE_TAX: "tax",
    OperationType.OPERATION_TYPE_DIVIDEND_TAX: "tax",
    OperationType.OPERATION_TYPE_DIVIDEND_TAX_PROGRESSIVE: "tax",
    OperationType.OPERATION_TYPE_BOND_TAX: "tax",
    OperationType.OPERATION_TYPE_BOND_TAX_PROGRESSIVE: "tax",
    OperationType.OPERATION_TYPE_BENEFIT_TAX: "tax",
    OperationType.OPERATION_TYPE_BENEFIT_TAX_PROGRESSIVE: "tax",
    OperationType.OPERATION_TYPE_SERVICE_FEE: "commission",
    OperationType.OPERATION_TYPE_ADVICE_FEE: "commission",

    # Cash operations
    OperationType.OPERATION_TYPE_INPUT: "deposit",
    OperationType.OPERATION_TYPE_OUTPUT: "withdrawal",

    # Securities transfer
    OperationType.OPERATION_TYPE_INPUT_SECURITIES: "securities_deposit",
    OperationType.OPERATION_TYPE_OUTPUT_SECURITIES: "securities_withdrawal",

    # Other income
    OperationType.OPERATION_TYPE_BOND_TAX: "tax",
    OperationType.OPERATION_TYPE_BOND_REPAYMENT: "bond_repayment",
    OperationType.OPERATION_TYPE_BOND_REPAYMENT_FULL: "bond_repayment",

    # Margin and repo
    OperationType.OPERATION_TYPE_MARGIN_FEE: "commission",
    OperationType.OPERATION_TYPE_OVERNIGHT: "overnight",

    # Corporate actions
    OperationType.OPERATION_TYPE_DIVIDEND_TRANSFER: "dividend",
    OperationType.OPERATION_TYPE_ACCRUING_VARMARGIN: "margin",
    OperationType.OPERATION_TYPE_WRITING_OFF_VARMARGIN: "margin",
}

# Mapping from Tinkoff exchange names to our exchange codes
TINKOFF_EXCHANGE_MAPPING = {
    "MOEX": "MOEX",
    "SPB": "SPB",
    "OTC": "OTC",
}

# Mapping from Tinkoff instrument types to our InstrumentCategory
TINKOFF_INSTRUMENT_TYPE_MAPPING = {
    "share": InstrumentCategory.STOCK,
    "stock": InstrumentCategory.STOCK,
    "bond": InstrumentCategory.BOND,
    "etf": InstrumentCategory.FUND,
    "currency": InstrumentCategory.CURRENCY,
    "futures": InstrumentCategory.COMMODITY,
    "option": InstrumentCategory.OTHER,
}


class TinkoffToken(BrokerBase):
    broker_code = "tinkoff"
    strategy = "api"
    supports_connections = True

    # Получение списка портфелей по токену
    async def get_accounts(self, **kwargs) -> list[AccountDict]:
        # здесь логика, например, получения списка аккаунтов по токену
        token = kwargs.get("access_token")
        if not token:
            raise Exception("Token not provided")

        with Client(token, target=INVEST_GRPC_API) as client:
            try:
                getAccountsRes = client.users.get_accounts()
                accounts = []
                for account in getAccountsRes.accounts:
                    if account.access_level.name != 'ACCOUNT_ACCESS_LEVEL_READ_ONLY':
                        raise Exception("We only allow read access tokens")
                    accounts.append({
                        'id': account.id,
                        'name': account.name,
                        'status': ConnectionStatus.ACTIVE
                    })
            except Exception as e:
                raise Exception(e.metadata.message)

        return accounts

    async def import_operations(self, **kwargs):
        portfolio = kwargs['portfolio']
        if not portfolio:
            raise Exception("portfolio is required")
        connection = kwargs['connection']
        if not connection:
            raise Exception("connection is required")
        db = kwargs.get('db')
        if not db:
            raise Exception("db (database session) is required")

        operations = []
        errors = []

        with Client(connection.access_token, target=INVEST_GRPC_API) as client:
            try:
                cursor = None
                has_next = True

                while has_next:
                    request = GetOperationsByCursorRequest(
                        account_id=connection.account_id,
                        cursor=cursor,
                        limit=1000,
                        state=1,
                        without_commissions=False,
                        without_trades=False,
                        without_overnights=True
                    )

                    response = client.operations.get_operations_by_cursor(request)

                    for item in response.items:
                        try:
                            operation, idenfifiers = self._convert_operation(item)
                            if operation:
                                operation['instrument_id'] = get_or_create_instrument(
                                    client, db, idenfifiers)
                                operation['portfolio_id'] = portfolio.id
                                operation['source'] = connection.id
                                operations.append(operation)
                        except Exception as e:
                            errors.append(f"Operation {item.id}: {str(e)}")

                    has_next = response.has_next
                    cursor = response.next_cursor if has_next else None

            except Exception as e:
                if hasattr(e, 'metadata') and hasattr(e.metadata, 'message'):
                    raise Exception(e.metadata.message)
                raise Exception(str(e))

        return operations, errors

    def _convert_operation(self, item) -> Optional[dict]:
        """
        Convert Tinkoff OperationItem to our universal operation format.

        Returns None if operation should be skipped.
        """
        # Extract basic info
        broker_operation_id = item.id
        timestamp = item.date
        operation_type = TINKOFF_OPERATION_TYPE_MAPPING.get(
            item.type, None)

        # Extract instrument info
        figi = item.figi if hasattr(item, 'figi') and item.figi else None
        instrument_uid = item.instrument_uid if hasattr(
            item, 'instrument_uid') and item.instrument_uid else None

        # Extract financial data
        quantity = item.quantity if hasattr(item, 'quantity') else None
        price = money_value_to_decimal(item.price) if hasattr(
            item, 'price') and item.price else None
        price_currency = get_currency_code(item.price) if hasattr(
            item, 'price') and item.price else None

        payment = money_value_to_decimal(item.payment) if hasattr(
            item, 'payment') and item.payment else None
        payment_currency = get_currency_code(item.payment) if hasattr(
            item, 'payment') and item.payment else None

        commission = money_value_to_decimal(item.commission) if hasattr(
            item, 'commission') and item.commission else None
        commission_currency = get_currency_code(item.commission) if hasattr(
            item, 'commission') and item.commission else None

        # Extract tax from child operations
        tax = None
        tax_currency = None
        if hasattr(item, 'child_operations') and item.child_operations:
            for child in item.child_operations:
                # Child operations for taxes
                child_payment = money_value_to_decimal(
                    child.payment) if child.payment else None
                if child_payment and child_payment < 0:  # Tax is negative
                    tax = abs(child_payment)
                    tax_currency = get_currency_code(child.payment)
                    break

        # Extract accrued interest (for bonds)
        accrued_interest = money_value_to_decimal(item.accrued_int) if hasattr(
            item, 'accrued_int') and item.accrued_int else None
        accrued_interest_currency = get_currency_code(item.accrued_int) if hasattr(
            item, 'accrued_int') and item.accrued_int else None

        # Description
        description = item.description if hasattr(
            item, 'description') and item.description else None
        name = item.name if hasattr(item, 'name') and item.name else None
        if name and description:
            description = f"{name}: {description}"
        elif name:
            description = name

        # Store raw data for debugging
        raw_data = {
            "id": broker_operation_id,
            "type": item.type,
            "date": item.date.isoformat() if item.date else None,
            "instrument_uid": instrument_uid,
            "figi": figi,
        }

        # Build operation dict
        operation = {
            "broker_operation_id": broker_operation_id,
            "timestamp": timestamp,
            "operation_type": operation_type,
            "quantity": quantity,
            "price": float(price) if price else None,
            "price_currency": price_currency,
            "payment": float(payment) if payment else None,
            "payment_currency": payment_currency,
            "commission": float(commission) if commission else None,
            "commission_currency": commission_currency,
            "tax": float(tax) if tax else None,
            "tax_currency": tax_currency,
            "accrued_interest": float(accrued_interest) if accrued_interest else None,
            "accrued_interest_currency": accrued_interest_currency,
            "description": description,
            "raw_data": raw_data
        }

        idenfifiers = {
            "instrument_uid": instrument_uid,
            "figi": figi,
            "exchange_code": "CURRENCY" if operation_type not in ['buy', 'sell'] else None,
            "code": payment_currency if operation_type not in ['buy', 'sell'] else None,
        }

        return operation, idenfifiers



def money_value_to_decimal(money: Optional[MoneyValue]) -> Optional[Decimal]:
    """
    Convert Tinkoff MoneyValue to Decimal.

    MoneyValue consists of:
    - units: integer part
    - nano: fractional part (1/10^9)

    Example: MoneyValue(units=123, nano=450000000) = 123.45
    """
    if money is None:
        return None

    return Decimal(money.units) + Decimal(money.nano) / Decimal(1_000_000_000)


def get_currency_code(money: Optional[MoneyValue]) -> Optional[str]:
    """
    Extract currency code from MoneyValue and convert to uppercase.

    Tinkoff returns lowercase currency codes (e.g., 'rub', 'usd', 'eur').
    We convert them to uppercase for consistency (RUB, USD, EUR).
    """
    if money is None or not money.currency:
        return None

    return money.currency.upper()


def get_or_create_instrument(client: Client, db: Session, identifiers: dict) -> int:
    # Check existing instruments based on identifiers
    instrument = utils.find_instrument(db, identifiers)
    if instrument:
        return instrument.id

    # If not found, fetch from Tinkoff API and create new instrument
    figi = identifiers.get('figi')
    instrument_uid = identifiers.get('instrument_uid')
    exchange_code = identifiers.get('exchange_code')
    code = identifiers.get('code')

    # Try to get instrument info from Tinkoff API
    tinkoff_instrument = None
    if instrument_uid:
        # Prefer instrument_uid as it's more reliable
        request = InstrumentRequest(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_UID,
            id=instrument_uid
        )
        response = client.instruments.get_instrument_by(request=request)
        tinkoff_instrument = response.instrument
    elif figi:
        # Fallback to FIGI
        request = InstrumentRequest(
            id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI,
            id=figi
        )
        response = client.instruments.get_instrument_by(request=request)
        tinkoff_instrument = response.instrument
    elif exchange_code and code:
        # Create currency new instrument
        instrument = Instrument(
            exchange_code=exchange_code,
            code=code,
            category=InstrumentCategory.CURRENCY,
            currency=code,
            status=InstrumentStatus.ACTIVE
        )

    if tinkoff_instrument:
        # Map Tinkoff exchange to our exchange code
        # Tinkoff returns exchange like "MOEX", "SPB", etc.
        exchange_code = TINKOFF_EXCHANGE_MAPPING.get(
            tinkoff_instrument.exchange,
            None
        )

        # Map Tinkoff instrument type to our category
        category = TINKOFF_INSTRUMENT_TYPE_MAPPING.get(
            tinkoff_instrument.instrument_type.lower(),
            None
        )

        if not exchange_code or not category:
            raise Exception(f"Could not map exchange_code or category for instrument: {tinkoff_instrument.ticker}")

        # Create new instrument
        instrument = Instrument(
            exchange_code=exchange_code,
            code=tinkoff_instrument.ticker,
            name=tinkoff_instrument.name,
            figi=tinkoff_instrument.figi if tinkoff_instrument.figi else None,
            isin=tinkoff_instrument.isin if tinkoff_instrument.isin else None,
            category=category,
            currency=tinkoff_instrument.currency.upper(
            ) if tinkoff_instrument.currency else None,
            status=InstrumentStatus.ACTIVE if tinkoff_instrument.api_trade_available_flag else InstrumentStatus.INACTIVE
        )

    if not instrument:
        raise Exception(f"Could not create new instrument for: {identifiers}")

    db.add(instrument)
    db.commit()
    db.refresh(instrument)

    return instrument.id

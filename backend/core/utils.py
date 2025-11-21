from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import insert
from backend.models import Portfolio, PortfolioConnection, User, Connection, Instrument


def get_or_create(db, model, defaults=None, **filters):
    instance = db.query(model).filter_by(**filters).first()
    if instance:
        return instance, False

    params = {**filters, **(defaults or {})}
    instance = model(**params)
    db.add(instance)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        instance = db.query(model).filter_by(**filters).first()
        return instance, False

    db.refresh(instance)
    return instance, True


def check_users_limit(client):
    if client.users_limit and client.users_count >= client.users_limit:
        raise HTTPException(403, "User limit reached")


def check_portfolios_limit(client, user):
    if client.user_portfolios_limit and user.portfolios_count >= client.user_portfolios_limit:
        raise HTTPException(
            403, f"Portfolio limit reached for user {user.external_id}")


def consume_api_request(client, db):
    if client.api_requests_limit is None:
        return
    if client.api_requests_remaining is None:
        client.api_requests_remaining = client.api_requests_limit
    if client.api_requests_remaining <= 0:
        raise HTTPException(429, "Daily API request limit reached")
    client.api_requests_remaining -= 1
    db.commit()


def create_and_link_portfolio(user: User, db: Session, connection: Connection | None):
    portfolio = Portfolio(
        user_id=user.id, name=f"Portfolio №{user.portfolios_count + 1} for user {user.id}")
    db.add(portfolio)
    db.flush()  # Get portfolio.id without committing
    # increase counter
    user.portfolios_count += 1
    db.add(user)
    # Link connection to portfolio
    if connection:
        portfolio_connection = PortfolioConnection(
            portfolio_id=portfolio.id,
            connection_id=connection.id
        )
        db.add(portfolio_connection)

    # commit changes
    db.commit()
    return portfolio

def link_portfolio_with_connection(db: Session, portfolio, connection):
    stmt = insert(PortfolioConnection).values(
        portfolio_id=portfolio.id,
        connection_id=connection.id
    )
    stmt = stmt.on_conflict_do_nothing(
        constraint='uq_portfolios_connections_pair'
    )
    db.execute(stmt)
    db.commit()

def find_instrument(db: Session, identifiers: dict):
    # Try to find by FIGI first (most common identifier)
    figi = identifiers.get('figi')
    if figi:
        instrument = db.query(Instrument).filter(
            Instrument.figi == figi).first()
        if instrument:
            return instrument

    # Try to find by ISIN
    isin = identifiers.get('isin')
    if isin:
        instrument = db.query(Instrument).filter(
            Instrument.isin == isin).first()
        if instrument:
            return instrument

    # Try to find by exchange_code + code
    exchange_code = identifiers.get('exchange_code')
    code = identifiers.get('code')
    if exchange_code and code:
        instrument = db.query(Instrument).filter(
            Instrument.exchange_code == exchange_code, Instrument.code == code).first()
        if instrument:
            return instrument
    return None

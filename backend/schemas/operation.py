from pydantic import BaseModel, Field
from typing import Optional
from decimal import Decimal
from datetime import datetime


# -----------------------------
# Payload для ручного ввода сделок и токенов
# -----------------------------
class OperationCreate(BaseModel):
    """Schema for creating an operation."""
    portfolio_id: int = Field(..., description="ID of the portfolio")
    instrument_id: int = Field(..., description="ID of the instrument")
    timestamp: datetime = Field(..., description="Operation timestamp")

    # Broker identification
    broker_operation_id: Optional[str] = Field(None, max_length=128, description="Broker's operation ID")
    # Operation type and state
    operation_type: Optional[str] = Field(None, max_length=32, description="Operation type: buy, sell, dividend, etc.")

    # Quantity and price
    quantity: Optional[Decimal] = Field(None, description="Quantity of instruments")
    price: Optional[Decimal] = Field(None, description="Price per unit")
    price_currency: Optional[str] = Field(None, max_length=3, description="Price currency code")

    # Commission
    commission: Optional[Decimal] = Field(None, description="Commission amount")
    commission_currency: Optional[str] = Field(None, max_length=3, description="Commission currency code")

    # Tax
    tax: Optional[Decimal] = Field(None, description="Tax amount")
    tax_currency: Optional[str] = Field(None, max_length=3, description="Tax currency code")

    # Accrued interest (for bonds)
    accrued_interest: Optional[Decimal] = Field(None, description="Accrued interest amount")
    accrued_interest_currency: Optional[str] = Field(None, max_length=3, description="Accrued interest currency code")

    # Payment (main financial field)
    payment: Optional[Decimal] = Field(None, description="Total payment amount")
    payment_currency: Optional[str] = Field(None, max_length=3, description="Payment currency code")

    # Additional info
    description: Optional[str] = Field(None, description="Operation description")

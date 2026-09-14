from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field


class LoanCreate(BaseModel):
    borrower_name: str = Field(min_length=1, max_length=200)
    loan_amount: Decimal = Field(gt=0, max_digits=14, decimal_places=2)
    property_city: str | None = Field(default=None, max_length=200)
    status: str = Field(default="PENDING", min_length=1, max_length=50)


class LoanResponse(BaseModel):
    id: int
    borrower_name: str
    loan_amount: Decimal
    property_city: str | None
    status: str
    created_at: datetime
    served_by: str
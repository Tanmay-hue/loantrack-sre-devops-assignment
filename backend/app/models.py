from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal


@dataclass
class Loan:
    id: int
    borrower_name: str
    loan_amount: Decimal
    property_city: str | None
    status: str
    created_at: datetime
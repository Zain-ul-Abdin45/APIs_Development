from pydantic import BaseModel, Field
from typing import Optional


class Account(BaseModel):
    account_id: str
    owner: str
    currency: str = "USD"
    balance: float
    status: str = "active"


class AccountSummary(BaseModel):
    account: Account
    transactions: list[dict]
    exchange_rate: Optional[float] = None
    exchange_currency: str = "EUR"

from pydantic import BaseModel
from datetime import datetime
from sqlalchemy import Column, DateTime, Float, String, text
from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass


class TransactionORM(Base):
    __tablename__ = "transactions"

    transaction_id = Column(String, primary_key=True)
    account_id = Column(String, nullable=False, index=True)
    amount = Column(Float, nullable=False)
    currency = Column(String, default="USD")
    created_at = Column(DateTime, server_default=text("NOW()"))


class Transaction(BaseModel):
    transaction_id: str
    account_id: str
    amount: float
    currency: str
    created_at: datetime

    model_config = {"from_attributes": True}

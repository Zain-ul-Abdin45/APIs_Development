import asyncio
from app.repositories.account_repo import find_account
from app.repositories.transaction_repo import get_transactions
from app.services.exchange_service import get_exchange_rate
from app.models.account import AccountSummary
from fastapi import HTTPException


async def get_account_summary(account_id: str, currency: str = "EUR") -> AccountSummary:
    # Fire all three I/O operations concurrently — none depends on the others
    account, transactions, exchange_rate = await asyncio.gather(
        find_account(account_id),
        get_transactions(account_id),
        get_exchange_rate("USD", currency),
    )

    if account is None:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")

    return AccountSummary(
        account=account,
        transactions=[t.model_dump() for t in transactions],
        exchange_rate=exchange_rate,
        exchange_currency=currency,
    )

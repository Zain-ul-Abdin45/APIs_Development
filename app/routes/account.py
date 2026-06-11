from fastapi import APIRouter, Query
from app.models.account import AccountSummary
from app.services.account_service import get_account_summary

router = APIRouter(prefix="/accounts", tags=["accounts"])


@router.get("/{account_id}/summary", response_model=AccountSummary)
async def account_summary(
    account_id: str,
    currency: str = Query(default="EUR", description="Target currency for exchange rate"),
):
    return await get_account_summary(account_id, currency)

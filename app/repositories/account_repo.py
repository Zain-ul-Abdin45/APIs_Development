from typing import Optional
from app.db.mongo import get_mongo_db
from app.models.account import Account


async def find_account(account_id: str) -> Optional[Account]:
    db = get_mongo_db()
    doc = await db["accounts"].find_one(
        {"account_id": account_id},
        {"_id": 0},  # never return Mongo's internal _id to callers
    )
    if doc is None:
        return None
    return Account(**doc)


async def upsert_account(account: Account) -> None:
    db = get_mongo_db()
    await db["accounts"].update_one(
        {"account_id": account.account_id},
        {"$set": account.model_dump()},
        upsert=True,
    )

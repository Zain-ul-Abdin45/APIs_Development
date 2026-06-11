from sqlalchemy import select
from app.db.postgres import get_session
from app.models.transaction import Transaction, TransactionORM


async def get_transactions(account_id: str) -> list[Transaction]:
    async with get_session() as session:
        result = await session.execute(
            select(TransactionORM)
            .where(TransactionORM.account_id == account_id)
            .order_by(TransactionORM.created_at.desc())
            .limit(50)
        )
        rows = result.scalars().all()
        return [Transaction.model_validate(row) for row in rows]

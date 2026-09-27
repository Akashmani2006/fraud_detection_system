from sqlalchemy.orm import Session

from app.database.models import Transaction


def get_recent_transactions(
    db: Session,
    user_id: str,
    limit: int = 10
):
    transactions = (
        db.query(Transaction)
        .filter(Transaction.user_id == user_id)
        .order_by(Transaction.timestamp.desc())
        .limit(limit)
        .all()
    )

    return transactions
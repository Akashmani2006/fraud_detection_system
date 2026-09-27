from app.database.database import SessionLocal
from app.tools.transaction_tools import get_recent_transactions


db = SessionLocal()

transactions = get_recent_transactions(
    db=db,
    user_id="U1001"
)

for transaction in transactions:
    print(
        transaction.amount,
        transaction.merchant_id,
        transaction.location
    )

db.close()
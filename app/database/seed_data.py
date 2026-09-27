from datetime import datetime, timedelta

from app.database.database import SessionLocal
from app.database.models import Transaction


db = SessionLocal()

now = datetime.utcnow()

transactions = [
    Transaction(
        user_id="U1001",
        amount=500,
        merchant_id="M101",
        location="Chennai",
        timestamp=now - timedelta(minutes=60)
    ),

    Transaction(
        user_id="U1001",
        amount=800,
        merchant_id="M102",
        location="Chennai",
        timestamp=now - timedelta(minutes=45)
    ),

    Transaction(
        user_id="U1001",
        amount=1200,
        merchant_id="M103",
        location="Chennai",
        timestamp=now - timedelta(minutes=30)
    ),

    Transaction(
        user_id="U1001",
        amount=75000,
        merchant_id="M501",
        location="New York",
        timestamp=now - timedelta(minutes=10)
    ),

    Transaction(
        user_id="U1001",
        amount=80000,
        merchant_id="M501",
        location="New York",
        timestamp=now
    )
]

db.add_all(transactions)
db.commit()

print("Sample transactions added successfully!")

db.close()
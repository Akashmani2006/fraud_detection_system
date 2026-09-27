import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.database.database import SessionLocal
from app.tools.transaction_tools import get_recent_transactions
from app.schemas.velocity_schema import VelocityAssessment


load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

structured_model = model.with_structured_output(
    VelocityAssessment
)


def run_velocity_agent(user_id: str):

    # 1. Open database session
    db = SessionLocal()

    # 2. Get recent transactions
    transactions = get_recent_transactions(
        db=db,
        user_id=user_id
    )

    # 3. Calculate actual facts from the database
    transaction_count = len(transactions)

    transaction_data = []

    for transaction in transactions:
        transaction_data.append({
            "amount": transaction.amount,
            "merchant_id": transaction.merchant_id,
            "location": transaction.location,
            "timestamp": str(transaction.timestamp)
        })

    db.close()

    # 4. Give actual database facts to Gemini
    prompt = f"""
You are the Velocity Risk Agent in a fraud detection system.

Analyze the user's transaction velocity using ONLY the
facts provided below.

IMPORTANT:
- Do not invent transactions.
- Do not claim multiple transactions unless transaction_count
  is greater than 1.
- Do not invent transaction frequency.
- Base your assessment only on the provided data.

Actual transaction count:
{transaction_count}

Transactions:
{transaction_data}

Determine whether the transaction activity shows
suspicious velocity or unusual transaction frequency.

Rules:
- If transaction_count == 1, there is no evidence of
  repeated transaction activity in the provided data.
- If transaction_count is greater than 1, consider the
  number of transactions and their timestamps.
- Do not assume suspicious behavior without evidence.

Return:
- risk_score between 0 and 1
- risk_level: LOW, MEDIUM, or HIGH
- reason explaining your assessment
- transaction_count
"""

    # 5. Ask Gemini for structured assessment
    result = structured_model.invoke(prompt)

    return result
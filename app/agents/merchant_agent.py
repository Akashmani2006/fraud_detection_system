import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas.merchant_schema import MerchantAssessment
from app.database.database import SessionLocal
from app.tools.transaction_tools import get_recent_transactions
from app.tools.merchant_tools import get_merchant_risk

load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

structured_model = model.with_structured_output(
    MerchantAssessment
)
def run_merchant_agent(user_id: str):

    db = SessionLocal()

    transactions = get_recent_transactions(
        db=db,
        user_id=user_id
    )

    db.close()

    print("Transactions received by Merchant Agent:")

    for transaction in transactions:
        print(
            f"Amount: ₹{transaction.amount}, "
            f"Merchant: {transaction.merchant_id}"
        )
    merchant_data = []

    for transaction in transactions:

        risk_info = get_merchant_risk(
            transaction.merchant_id
        )

        merchant_data.append(risk_info)

    print("\nMerchant risk information:")

    for merchant in merchant_data:
        print(merchant)
    prompt = f"""
You are the Merchant Risk Agent in a fraud detection system.

Analyze the merchants involved in the user's recent transactions.

Determine whether the merchant activity indicates fraud risk.

Consider:
- Merchant risk scores
- Merchant risk levels
- Repeated transactions with the same merchant
- Whether a high-risk merchant appears in recent transactions

Merchant risk information:
{merchant_data}

Return:
- risk_score between 0 and 1
- risk_level: LOW, MEDIUM, or HIGH
- reason explaining your assessment
- merchant_id
"""

    result = structured_model.invoke(prompt)

    return result
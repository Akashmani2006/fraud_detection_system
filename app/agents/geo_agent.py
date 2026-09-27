import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas.geo_schema import GeoAssessment
from app.database.database import SessionLocal
from app.tools.transaction_tools import get_recent_transactions
from app.tools.geo_tools import get_location_info

load_dotenv()


model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)


structured_model = model.with_structured_output(
    GeoAssessment
)
def run_geo_agent(user_id: str):

    db = SessionLocal()

    transactions = get_recent_transactions(
        db=db,
        user_id=user_id
    )

    db.close()

    print("Transactions received by Geo Agent:")

    for transaction in transactions:
        print(
            f"Amount: ₹{transaction.amount}, "
            f"Location: {transaction.location}"
        )

    location_data = []

    for transaction in transactions:

        info = get_location_info(
            transaction.location
        )

        location_data.append({
            "location": transaction.location,
            "country": info["country"],
            "city": info["city"],
            "risk_region": info["risk_region"]
        })

    print("\nLocation information:")

    for location in location_data:
        print(location)
    prompt = f"""
You are the Geo Risk Agent in a fraud detection system.

Analyze the geographic behavior of the user's recent transactions.

Determine whether there is suspicious geographic activity.

Consider:
- Changes between locations
- Changes between countries
- Unusual geographic movement
- How quickly the locations changed

Transaction location information:
{location_data}

Return:
- risk_score between 0 and 1
- risk_level: LOW, MEDIUM, or HIGH
- reason explaining your assessment
- current_location
- previous_location
"""
    result = structured_model.invoke(prompt)

    return result
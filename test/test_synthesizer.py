from app.agents.synthesizer_agent import run_synthesizer_agent


velocity_result = {
    "risk_score": 0.85,
    "risk_level": "HIGH",
    "reason": "Multiple high-value transactions occurred within a very short timeframe.",
    "transaction_count": 5
}

geo_result = {
    "risk_score": 0.95,
    "risk_level": "HIGH",
    "reason": "Impossible travel detected between New York and Chennai.",
    "current_location": "Chennai, India",
    "previous_location": "New York, USA"
}

merchant_result = {
    "risk_score": 0.90,
    "risk_level": "HIGH",
    "reason": "Repeated transactions involve high-risk merchant M501.",
    "merchant_id": "M501"
}


result = run_synthesizer_agent(
    velocity_result,
    geo_result,
    merchant_result
)


print("\nSYNTHESIZER RESULT")
print("Risk Score:", result.risk_score)
print("Risk Level:", result.risk_level)
print("Decision:", result.decision)
print("Reason:", result.reason)
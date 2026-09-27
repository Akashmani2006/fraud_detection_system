from app.agents.merchant_agent import run_merchant_agent


result = run_merchant_agent("U1001")

print("\nMerchant Risk Score:", result.risk_score)
print("Merchant Risk Level:", result.risk_level)
print("Reason:", result.reason)
print("Merchant ID:", result.merchant_id)
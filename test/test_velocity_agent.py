from app.agents.velocity_agent import run_velocity_agent

result = run_velocity_agent("U2001")

print("\nVELOCITY RESULT")
print("Risk Score:", result.risk_score)
print("Risk Level:", result.risk_level)
print("Reason:", result.reason)
print("Transaction Count:", result.transaction_count)
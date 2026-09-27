from app.agents.geo_agent import run_geo_agent


result = run_geo_agent("U1001")

print("\nGeo Risk Score:", result.risk_score)
print("Geo Risk Level:", result.risk_level)
print("Reason:", result.reason)
print("Current Location:", result.current_location)
print("Previous Location:", result.previous_location)

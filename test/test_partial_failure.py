import app.graph.nodes as nodes


# Simulate an agent failure
def simulated_failure(*args, **kwargs):
    raise Exception("Simulated agent failure")


# Replace the real agents temporarily
nodes.run_velocity_agent = simulated_failure
nodes.run_geo_agent = simulated_failure
nodes.run_merchant_agent = simulated_failure


state = {
    "user_id": "U3001",
    "alert_id": 7
}


print("\n--- VELOCITY FAILURE TEST ---")
print(nodes.velocity_node(state))

print("\n--- GEO FAILURE TEST ---")
print(nodes.geo_node(state))

print("\n--- MERCHANT FAILURE TEST ---")
print(nodes.merchant_node(state))
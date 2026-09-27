from app.graph.nodes import velocity_node
from app.graph.state import FraudState
from app.graph.nodes import geo_node
from app.graph.nodes import merchant_node

state: FraudState = {
    "user_id": "U1001"
}

# result = velocity_node(state)
# result = geo_node(state)
result = merchant_node(state)


print(result)
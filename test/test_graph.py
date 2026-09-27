from app.graph.graph import app
from app.graph.state import FraudState

initial_state: FraudState = {
    "user_id": "U1001"
}

result = app.invoke(initial_state)

print("\nFINAL STATE:")
print(result)
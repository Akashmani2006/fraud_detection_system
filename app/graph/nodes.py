from app.tools.timeout_tools import run_with_timeout
# -------------------------
# Velocity Agent Node
# -------------------------

from app.agents.velocity_agent import run_velocity_agent
from app.graph.state import FraudState


def velocity_node(state: FraudState):

    try:

        result = run_with_timeout(
             run_velocity_agent,
             30,
            state["user_id"]
            )

        return {
            "velocity_result": result.model_dump()
        }

    except Exception as e:

        print("Velocity Agent failed:", e)

        return {
            "velocity_result": {
                "risk_score": 0.5,
                "risk_level": "MEDIUM",
                "reason": "Velocity Agent failed. Assessment has degraded confidence.",
                "transaction_count": 0
            }
        }

# -------------------------
# Geo Agent Node
# -------------------------

from app.agents.geo_agent import run_geo_agent


def geo_node(state: FraudState):

    try:

        result = run_with_timeout(
            run_geo_agent,
            30,
            state["user_id"]
           )

        return {
            "geo_result": result.model_dump()
        }

    except Exception as e:

        print("Geo Agent failed:", e)

        return {
            "geo_result": {
                "risk_score": 0.5,
                "risk_level": "MEDIUM",
                "reason": "Geo Agent failed. Assessment has degraded confidence.",
                "current_location": "UNKNOWN",
                "previous_location": "UNKNOWN"
            }
        }

# -------------------------
# Merchant Agent Node
# -------------------------

from app.agents.merchant_agent import run_merchant_agent
def merchant_node(state: FraudState):

    try:

        result = run_with_timeout(
            run_merchant_agent,
            30,
            state["user_id"]
)

        return {
            "merchant_result": result.model_dump()
        }

    except Exception as e:

        print("Merchant Agent failed:", e)

        return {
            "merchant_result": {
                "risk_score": 0.5,
                "risk_level": "MEDIUM",
                "reason": "Merchant Agent failed. Assessment has degraded confidence.",
                "merchant_id": "UNKNOWN"
            }
        }


# -------------------------
# Merge Node
# -------------------------

from app.agents.synthesizer_agent import run_synthesizer_agent
from app.database.database import SessionLocal
from app.tools.risk_assessment_tools import save_risk_assessment
from app.tools.case_tools import create_case


def merge_node(state: FraudState):

    # Run Gemini Synthesizer
    result = run_synthesizer_agent(
        velocity_result=state["velocity_result"],
        geo_result=state["geo_result"],
        merchant_result=state["merchant_result"]
    )

    # Open database
    db = SessionLocal()

    # Save Velocity assessment
    save_risk_assessment(
        db=db,
        alert_id=state["alert_id"],
        agent_type="velocity",
        risk_score=state["velocity_result"]["risk_score"],
        risk_level=state["velocity_result"]["risk_level"],
        reason=state["velocity_result"]["reason"]
    )

    # Save Geo assessment
    save_risk_assessment(
        db=db,
        alert_id=state["alert_id"],
        agent_type="geo",
        risk_score=state["geo_result"]["risk_score"],
        risk_level=state["geo_result"]["risk_level"],
        reason=state["geo_result"]["reason"]
    )

    # Save Merchant assessment
    save_risk_assessment(
        db=db,
        alert_id=state["alert_id"],
        agent_type="merchant",
        risk_score=state["merchant_result"]["risk_score"],
        risk_level=state["merchant_result"]["risk_level"],
        reason=state["merchant_result"]["reason"]
    )

    # Create case only when escalation is required
    if result.decision == "ESCALATE":

        case = create_case(
            db=db,
            alert_id=state["alert_id"],
            risk_score=result.risk_score,
            decision=result.decision
        )

        print(f"Case created: {case.id}")

    db.close()

    return {
        "final_risk_score": result.risk_score,
        "final_risk_level": result.risk_level,
        "final_reason": result.reason,
        "decision": result.decision
    }


# -------------------------
# Auto Clear Node
# -------------------------

def auto_clear_node(state: FraudState):

    print("Transaction automatically cleared.")

    return {}


# -------------------------
# Escalate Node
# -------------------------

def escalate_node(state: FraudState):

    print("Transaction escalated for human review.")

    return {}
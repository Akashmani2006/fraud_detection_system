from typing import TypedDict


class FraudState(TypedDict, total=False):
    user_id: str
    alert_id: int
    velocity_result: dict
    geo_result: dict
    merchant_result: dict

    final_risk_score: float
    final_risk_level: str
    final_reason: str
    decision: str
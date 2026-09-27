from sqlalchemy.orm import Session
from app.database.models import RiskAssessment


def save_risk_assessment(
    db: Session,
    alert_id: int,
    agent_type: str,
    risk_score: float,
    risk_level: str,
    reason: str
):
    assessment = RiskAssessment(
        alert_id=alert_id,
        agent_type=agent_type,
        risk_score=risk_score,
        risk_level=risk_level,
        reason=reason
    )

    db.add(assessment)
    db.commit()
    db.refresh(assessment)

    return assessment
from sqlalchemy.orm import Session
from app.database.models import Case


def create_case(
    db: Session,
    alert_id: int,
    risk_score: float,
    decision: str
):
    case = Case(
        alert_id=alert_id,
        risk_score=risk_score,
        decision=decision,
        status="OPEN"
    )

    db.add(case)
    db.commit()
    db.refresh(case)

    return case
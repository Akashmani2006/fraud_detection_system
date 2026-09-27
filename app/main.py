from fastapi import FastAPI
from pydantic import BaseModel

from app.database.database import SessionLocal
from app.database.models import Transaction, Alert, Case, CaseNote
from app.graph.graph import app as fraud_graph


app = FastAPI(
    title="Fraud Detection Triage System",
    description="Multi-agent fraud detection and triage API",
    version="1.0.0"
)


class AlertRequest(BaseModel):
    user_id: str
    amount: float
    merchant_id: str
    location: str
    alert_type: str = "FRAUD_SUSPECTED"
    idempotency_key: str

class CaseNoteRequest(BaseModel):
    author: str
    note: str

@app.get("/")
def root():
    return {
        "message": "Fraud Detection Triage System is running"
    }
@app.post("/alerts/ingest")
def ingest_alert(request: AlertRequest):

    db = SessionLocal()

    # Check if this alert was already received
    existing_alert = (
        db.query(Alert)
        .filter(Alert.idempotency_key == request.idempotency_key)
        .first()
    )

    if existing_alert:

        transaction_id = existing_alert.transaction_id
        alert_id = existing_alert.id

        db.close()

        return {
            "message": "Alert already exists",
            "alert_id": alert_id,
            "transaction_id": transaction_id
        }

    # Create new transaction
    transaction = Transaction(
        user_id=request.user_id,
        amount=request.amount,
        merchant_id=request.merchant_id,
        location=request.location
    )

    db.add(transaction)
    db.commit()
    db.refresh(transaction)

    # Create new alert
    alert = Alert(
        transaction_id=transaction.id,
        alert_type=request.alert_type,
        status="OPEN",
        idempotency_key=request.idempotency_key
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    transaction_id = transaction.id
    alert_id = alert.id

    db.close()

    return {
        "message": "Alert ingested successfully",
        "alert_id": alert_id,
        "transaction_id": transaction_id
    }
@app.post("/alerts/{alert_id}/triage")
def triage_alert(alert_id: int):

    db = SessionLocal()

    # Find the alert
    alert = db.query(Alert).filter(Alert.id == alert_id).first()

    if not alert:
        db.close()
        return {"error": "Alert not found"}

    # Find the transaction connected to this alert
    transaction = (
        db.query(Transaction)
        .filter(Transaction.id == alert.transaction_id)
        .first()
    )

    if not transaction:
        db.close()
        return {"error": "Transaction not found"}

    user_id = transaction.user_id

    db.close()

    # Send both user_id and alert_id to LangGraph
    initial_state = {
        "user_id": user_id,
        "alert_id": alert_id
    }

    # Run the fraud detection graph
    result = fraud_graph.invoke(initial_state)

    return {
        "alert_id": alert_id,
        "risk_score": result["final_risk_score"],
        "risk_level": result["final_risk_level"],
        "decision": result["decision"],
        "reason": result["final_reason"]
    }
@app.get("/cases/{case_id}")
def get_case(case_id: int):

    db = SessionLocal()

    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        db.close()
        return {"error": "Case not found"}

    notes = []

    for note in case.notes:
        notes.append({
            "note_id": note.id,
            "author": note.author,
            "note": note.note,
            "created_at": str(note.created_at)
        })

    response = {
        "case_id": case.id,
        "alert_id": case.alert_id,
        "risk_score": case.risk_score,
        "decision": case.decision,
        "status": case.status,
        "created_at": str(case.created_at),
        "notes": notes
    }

    db.close()

    return response
@app.post("/cases/{case_id}/notes")
def add_case_note(case_id: int, request: CaseNoteRequest):

    db = SessionLocal()

    # Check whether the case exists
    case = db.query(Case).filter(Case.id == case_id).first()

    if not case:
        db.close()
        return {"error": "Case not found"}

    # Create the case note
    note = CaseNote(
        case_id=case_id,
        author=request.author,
        note=request.note
    )

    db.add(note)
    db.commit()
    db.refresh(note)

    response = {
        "message": "Case note added successfully",
        "note_id": note.id,
        "case_id": note.case_id,
        "author": note.author,
        "note": note.note,
        "created_at": str(note.created_at)
    }

    db.close()

    return response
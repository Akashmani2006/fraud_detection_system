from datetime import datetime

from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.database.database import Base


# 1. Transactions
class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    merchant_id = Column(String, nullable=False)
    location = Column(String, nullable=False)
    timestamp = Column(DateTime, default=datetime.utcnow)

    alerts = relationship("Alert", back_populates="transaction")


# 2. Fraud Alerts
class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    transaction_id = Column(Integer, ForeignKey("transactions.id"))
    alert_type = Column(String, nullable=False)
    status = Column(String, default="OPEN")
    created_at = Column(DateTime, default=datetime.utcnow)
    idempotency_key = Column(String, unique=True, nullable=False)
    transaction = relationship("Transaction", back_populates="alerts")
    risk_assessments = relationship(
        "RiskAssessment",
        back_populates="alert"
    )
    cases = relationship("Case", back_populates="alert")


# 3. Risk Assessments
class RiskAssessment(Base):
    __tablename__ = "risk_assessments"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))

    agent_type = Column(String, nullable=False)
    risk_score = Column(Float, nullable=False)
    risk_level = Column(String, nullable=False)
    reason = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", back_populates="risk_assessments")


# 4. Cases
class Case(Base):
    __tablename__ = "cases"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))

    risk_score = Column(Float, nullable=False)
    decision = Column(String, nullable=False)
    status = Column(String, default="OPEN")

    created_at = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert", back_populates="cases")
    notes = relationship("CaseNote", back_populates="case")


# 5. Case Notes
class CaseNote(Base):
    __tablename__ = "case_notes"

    id = Column(Integer, primary_key=True, index=True)
    case_id = Column(Integer, ForeignKey("cases.id"))

    author = Column(String, nullable=False)
    note = Column(String, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    case = relationship("Case", back_populates="notes")
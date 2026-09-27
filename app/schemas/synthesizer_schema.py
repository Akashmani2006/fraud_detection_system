from typing import Literal
from pydantic import BaseModel, Field


class SynthesizerAssessment(BaseModel):
    risk_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Final fraud risk score between 0 and 1"
    )

    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

    decision: Literal["AUTO_CLEAR", "ESCALATE"]

    reason: str
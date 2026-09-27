from typing import Literal
from pydantic import BaseModel, Field


class MerchantAssessment(BaseModel):

    risk_score: float = Field(
        ge=0.0,
        le=1.0,
        description="Risk score between 0 and 1"
    )

    risk_level: Literal["LOW", "MEDIUM", "HIGH"]

    reason: str

    merchant_id: str
import os

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

from app.schemas.synthesizer_schema import SynthesizerAssessment


load_dotenv()

model = ChatGoogleGenerativeAI(
    model="gemini-3.5-flash-lite",
    google_api_key=os.getenv("GEMINI_API_KEY")
)

structured_model = model.with_structured_output(
    SynthesizerAssessment
)


def run_synthesizer_agent(
    velocity_result: dict,
    geo_result: dict,
    merchant_result: dict
):
    prompt = f"""
You are the Synthesizer Agent in a fraud detection system.

You receive the assessments produced by three specialist agents:

1. Velocity Risk Agent
{velocity_result}

2. Geo Risk Agent
{geo_result}

3. Merchant Risk Agent
{merchant_result}

Your job is to combine these independent assessments
and produce one final fraud risk assessment.

Consider:
- The risk score from each agent
- The risk level from each agent
- The reasons provided by each agent
- Whether multiple agents identify related suspicious behavior
- The overall strength of the evidence

IMPORTANT:
- Some specialist agents may have failed.
- If an agent's reason contains "degraded confidence", treat that
  assessment as uncertain evidence.
- Do not treat a fallback score of 0.5 as strong evidence of fraud.
- Base the final decision primarily on the specialist agents that
  completed successfully.
- Mention degraded confidence in the final reason when applicable.


Return:
- risk_score between 0 and 1
- risk_level: LOW, MEDIUM, or HIGH
- decision: AUTO_CLEAR or ESCALATE
- reason explaining the combined assessment
"""

    result = structured_model.invoke(prompt)

    return result
from typing import Dict
from app.services.groq_client import get_groq_client

def generate_insights(eda: Dict, ml_results: Dict, goal: str = "maximize_conversions") -> str:
    client = get_groq_client("openai/gpt-oss-120b")

    kpis = eda.get("kpis", {})
    classifier = ml_results.get("campaign_classifier", {})

    prompt = f"""
    You are a senior performance marketing analyst.

    Business goal: {goal}

    KPIs summary (JSON):
    {kpis}

    Model results (JSON):
    {classifier}

    Based on this, write a concise but deep analysis:
    - Overall performance
    - Which channels/campaigns are strong vs weak
    - Any trends you can infer from the metrics
    - Risks or red flags
    

    Write in bullet points, plain language, no fluff.
    """

    resp = client.invoke(prompt)
    return resp.content

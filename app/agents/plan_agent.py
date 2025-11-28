from typing import Dict
from app.services.groq_client import get_groq_client

def generate_plan(insights: str, ml_results: Dict, goal: str = "maximize_conversions") -> str:
    client = get_groq_client("openai/gpt-oss-120b")

    prompt = f"""
    You are a growth strategist for performance marketing who has studied Alex Hormozi's 100M offer and 100M leads.

    Goal: {goal}

    Analytical insights:
    {insights}

    Model results:
    {ml_results}

    Create a 3-part action plan Inspired with Alex Hormozi's thought process and words:
    1) Immediate changes (this week) – concrete actions like "pause X", "increase budget on Y by 20%"
    2) Experiments (this month) – A/B tests, new creatives, new audiences
    3) Strategic shifts (next 1–3 months) – e.g., channel mix, funnel improvements

    Use numbered bullets. Be specific with what to do and why.
    """

    resp = client.invoke(prompt)
    return resp.content

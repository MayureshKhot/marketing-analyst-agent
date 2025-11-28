import pandas as pd
from app.services.groq_client import get_groq_client
import json, re

MARKETING_ROLES = [
    "date", "channel", "campaign", "ad_group",
    "spend", "impressions", "clicks",
    "conversions", "revenue", "device",
    "geo", "audience", "landing_page"
]

def infer_schema_with_llm(columns: list[str]) -> dict:
    client = get_groq_client()
    prompt = f"""
    You are mapping CSV columns to marketing analytics roles.

    Return ONLY valid JSON. 
    Do not explain anything. 
    Do not use code blocks. 
    If you can't map a role, set it to null.

    CSV columns: {columns}

    Roles: {MARKETING_ROLES}

    Return exactly this format:
    {{
    "date": "...",
    "channel": "...",
    "campaign": "...",
    ...
    }}

    """
    resp = client.invoke(prompt)
    
    raw = resp.content

    # remove codeblocks if present
    raw = raw.strip().replace("```json", "").replace("```", "").strip()

    # extract JSON with regex (failsafe)
    json_match = re.search(r"\{(.|\n)*\}", raw)
    if not json_match:
        print("\n----- LLM RAW RESPONSE -----\n", raw)
        raise ValueError("Groq did not return JSON. Fix prompt or inspect response.")

    clean_json = json_match.group(0)

    return json.loads(clean_json)


def load_and_infer_schema(filepath: str) -> tuple[pd.DataFrame, dict]:
    df = pd.read_csv(filepath)
    # basic cleaning
    df = df.dropna(how="all")
    df.columns = [c.strip() for c in df.columns]
    schema = infer_schema_with_llm(list(df.columns))
    return df, schema

import pandas as pd
from typing import Dict
from app.services.viz_service import plot_spend_vs_revenue

def compute_basic_kpis(df: pd.DataFrame, schema: Dict) -> Dict:
    s = schema
    out = {}

    spend_col = s.get("spend")
    clicks_col = s.get("clicks")
    impressions_col = s.get("impressions")
    conv_col = s.get("conversions")
    rev_col = s.get("revenue")

    if spend_col and rev_col:
        total_spend = df[spend_col].sum()
        total_rev = df[rev_col].sum()
        out["total_spend"] = float(total_spend)
        out["total_revenue"] = float(total_rev)
        out["roas"] = float(total_rev / total_spend) if total_spend > 0 else None

    if clicks_col and impressions_col:
        total_clicks = df[clicks_col].sum()
        total_impressions = df[impressions_col].sum()
        out["ctr"] = float(total_clicks / total_impressions) if total_impressions > 0 else None

    if spend_col and clicks_col:
        total_spend = df[spend_col].sum()
        total_clicks = df[clicks_col].sum()
        out["cpc"] = float(total_spend / total_clicks) if total_clicks > 0 else None

    if conv_col and clicks_col:
        total_conv = df[conv_col].sum()
        total_clicks = df[clicks_col].sum()
        out["conversion_rate"] = float(total_conv / total_clicks) if total_clicks > 0 else None

    return out

def run_eda(df: pd.DataFrame, schema: Dict) -> Dict:
    kpis = compute_basic_kpis(df, schema)
    chart_path = plot_spend_vs_revenue(df, schema)
    return {
        "kpis": kpis,
        "charts": {
            "spend_vs_revenue": chart_path
        }
    }

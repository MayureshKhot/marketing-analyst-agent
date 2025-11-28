import pandas as pd
from typing import Dict

def add_basic_features(df: pd.DataFrame, schema: Dict) -> pd.DataFrame:
    df = df.copy()
    date_col = schema.get("date")
    if date_col:
        df[date_col] = pd.to_datetime(df[date_col])
        df["day_of_week"] = df[date_col].dt.dayofweek
        df["is_weekend"] = df["day_of_week"].isin([5, 6]).astype(int)

    spend_col = schema.get("spend")
    clicks_col = schema.get("clicks")
    impressions_col = schema.get("impressions")
    conv_col = schema.get("conversions")

    if spend_col and impressions_col:
        df["cpm"] = df[spend_col] * 1000 / df[impressions_col].replace(0, 1)

    if spend_col and clicks_col:
        df["cpc"] = df[spend_col] / df[clicks_col].replace(0, 1)

    if clicks_col and impressions_col:
        df["ctr"] = df[clicks_col] / df[impressions_col].replace(0, 1)

    if conv_col and clicks_col:
        df["cr"] = df[conv_col] / df[clicks_col].replace(0, 1)

    return df

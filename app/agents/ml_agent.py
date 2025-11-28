import pandas as pd
from typing import Dict
from app.utils.feature_engineering import add_basic_features
from app.models.campaign_classifier import train_campaign_classifier

def run_ml(df: pd.DataFrame, schema: Dict) -> Dict:
    df_fe = add_basic_features(df, schema)
    classifier_result = train_campaign_classifier(df_fe, schema)
    return {
        "campaign_classifier": classifier_result
    }

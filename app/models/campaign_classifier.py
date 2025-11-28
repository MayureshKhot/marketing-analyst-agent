import pandas as pd
from typing import Dict
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

def train_campaign_classifier(df: pd.DataFrame, schema: Dict) -> Dict:
    s = schema
    spend_col = s.get("spend")
    rev_col = s.get("revenue")
    campaign_col = s.get("campaign")

    if not all([spend_col, rev_col, campaign_col]):
        return {"error": "Missing required columns for classifier"}

    df = df.copy()
    grouped = df.groupby(campaign_col)[[spend_col, rev_col]].sum()
    grouped["roas"] = grouped[rev_col] / grouped[spend_col].replace(0, 1)
    # Binary label: good if ROAS > 2 (tune later)
    grouped["label"] = (grouped["roas"] > 2.0).astype(int)

    grouped = grouped.reset_index()

    feature_cols = [spend_col, rev_col]
    X = grouped[feature_cols]
    y = grouped["label"]

    if y.nunique() < 2:
        return {"error": "Not enough variation for training"}

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    clf = RandomForestClassifier(n_estimators=100, random_state=42)
    clf.fit(X_train, y_train)
    acc = clf.score(X_test, y_test)

    grouped["pred_label"] = clf.predict(X)

    good_campaigns = grouped[grouped["pred_label"] == 1][campaign_col].tolist()
    bad_campaigns = grouped[grouped["pred_label"] == 0][campaign_col].tolist()

    return {
        "accuracy": float(acc),
        "good_campaigns": good_campaigns,
        "bad_campaigns": bad_campaigns,
    }

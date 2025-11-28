import plotly.graph_objects as go
import pandas as pd
import os

def plot_spend_vs_revenue(df, schema, output_dir="plots"):
    os.makedirs(output_dir, exist_ok=True)

    date_col = schema.get("date")
    spend_col = schema.get("spend")
    rev_col = schema.get("revenue")

    df[date_col] = pd.to_datetime(df[date_col])
    summary = df.groupby(date_col)[[spend_col, rev_col]].sum().reset_index()

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=summary[date_col], y=summary[spend_col],
                             mode='lines+markers', name='Spend'))
    fig.add_trace(go.Scatter(x=summary[date_col], y=summary[rev_col],
                             mode='lines+markers', name='Revenue'))

    fig.update_layout(
        title="Spend vs Revenue Over Time",
        xaxis_title="Date",
        yaxis_title="Amount",
        template="plotly_white"
    )

    output_path = os.path.join(output_dir, "spend_vs_revenue.png")
    fig.write_image(output_path)

    return output_path

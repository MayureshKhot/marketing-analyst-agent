# ui/app.py
import streamlit as st
import requests

BACKEND_URL = "http://127.0.0.1:8000"

st.title("Marketing Analytics Agent")

uploaded_file = st.file_uploader("Upload marketing CSV", type=["csv"])

if uploaded_file is not None:
    if st.button("Run Full Analysis"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        with st.spinner("Analyzing..."):
            resp = requests.post(f"{BACKEND_URL}/analyze/full", files=files)
        if resp.status_code == 200:
            data = resp.json()
            st.subheader("KPIs")
            st.json(data.get("eda", {}).get("kpis", {}))

            charts = data.get("eda", {}).get("charts", {})
            spend_chart = charts.get("spend_vs_revenue")
            if spend_chart:
                st.image(spend_chart, caption="Spend vs Revenue")

            st.subheader("Model Results")
            st.json(data.get("ml_results", {}))

            st.subheader("Insights")
            st.markdown(data.get("insights", ""))

            st.subheader("Action Plan")
            st.markdown(data.get("plan", ""))
        else:
            st.error(f"Error: {resp.text}")

    if st.button("Download PDF Report"):
        files = {"file": (uploaded_file.name, uploaded_file.getvalue(), "text/csv")}
        r = requests.post(f"{BACKEND_URL}/analyze/report", files=files)
        if r.status_code == 200:
            st.download_button(
                label="Download Report",
                data=r.content,
                file_name="marketing_report.pdf",
                mime="application/pdf"
            )
        else:
            st.error("Failed to generate report")

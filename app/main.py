# app/main.py
from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import os
from app.utils.file_utils import save_upload
from app.agents.ingestion_agent import load_and_infer_schema
from app.agents.ingestion_agent import load_and_infer_schema
from app.agents.eda_agent import run_eda
from app.services.langgraph_flow import build_graph
from dotenv import load_dotenv
from fastapi.responses import FileResponse
from app.agents.insight_agent import generate_insights
from app.agents.plan_agent import generate_plan
from app.agents.ml_agent import run_ml
from app.agents.report_agent import generate_html_report

load_dotenv()
app = FastAPI(title="Marketing Analytics Agent")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_csv(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    df = pd.read_csv(filepath)
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "file_path": filepath,
    }

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.post("/analyze/ingest")
async def ingest(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    df, schema = load_and_infer_schema(filepath)
    return {
        "rows": len(df),
        "columns": list(df.columns),
        "schema": schema,
        "file_path": filepath,
    }

@app.post("/analyze/eda")
async def analyze_eda(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    df, schema = load_and_infer_schema(filepath)
    eda_result = run_eda(df, schema)
    return {
        "schema": schema,
        "eda": eda_result,
    }

graph_app = build_graph()

@app.post("/analyze/full")
async def analyze_full(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    result = graph_app.invoke({"filepath": filepath})
    # Can't serialize df directly, so pop it
    result.pop("df", None)
    return result

@app.post("/analyze/report")
async def generate_report(file: UploadFile = File(...)):
    filepath = await save_upload(file)
    
    df, schema = load_and_infer_schema(filepath)
    eda = run_eda(df, schema)
    ml_results = run_ml(df, schema)
    
    insights = generate_insights(eda, ml_results)
    plan = generate_plan(insights, ml_results)
    
    charts = [
        eda["charts"]["spend_vs_revenue"],
        # add more charts here
    ]
    
    report_path = generate_html_report(
        eda["kpis"],
        insights,
        plan,
        charts,
        output_path="reports/marketing_report.pdf"
    )
    
    return FileResponse(report_path, media_type="application/pdf")
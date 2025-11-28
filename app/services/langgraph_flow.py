from langgraph.graph import StateGraph
from typing import TypedDict, Dict, Any
import pandas as pd

from app.agents.ingestion_agent import load_and_infer_schema
from app.agents.eda_agent import run_eda
# ml_agent, insight_agent, plan_agent to be added
from app.agents.ml_agent import run_ml
from app.agents.insight_agent import generate_insights
from app.agents.plan_agent import generate_plan


class PipelineState(TypedDict, total=False):
    filepath: str
    df: pd.DataFrame
    schema: Dict[str, Any]
    eda: Dict[str, Any]
    ml_results: Dict[str, Any]
    insights: str
    plan: str

def ingestion_node(state: PipelineState) -> PipelineState:
    df, schema = load_and_infer_schema(state["filepath"])
    state["df"] = df
    state["schema"] = schema
    return state

def eda_node(state: PipelineState) -> PipelineState:
    df = state["df"]
    schema = state["schema"]
    eda = run_eda(df, schema)
    state["eda"] = eda
    return state

def build_graph():
    workflow = StateGraph(PipelineState)
    workflow.add_node("ingestion", ingestion_node)
    workflow.add_node("eda", eda_node)
    # later: workflow.add_node("ml", ml_node) etc. (ADDED BELOW)
    workflow.add_node("ml", ml_node)
    workflow.add_edge("eda", "ml")


    workflow.set_entry_point("ingestion")
    workflow.add_edge("ingestion", "eda")
    # later edges: "eda" -> "ml" -> "insight" -> "plan" (ADDED BELOW)
    workflow.add_node("insight", insight_node)
    workflow.add_node("plan", plan_node)
    
    workflow.add_edge("ml", "insight")
    workflow.add_edge("insight", "plan")


    app = workflow.compile()
    return app

def ml_node(state: PipelineState) -> PipelineState:
    df = state["df"]
    schema = state["schema"]
    ml_results = run_ml(df, schema)
    state["ml_results"] = ml_results
    return state

def insight_node(state: PipelineState) -> PipelineState:
    eda = state.get("eda", {})
    ml_results = state.get("ml_results", {})
    insights = generate_insights(eda, ml_results)
    state["insights"] = insights
    return state

def plan_node(state: PipelineState) -> PipelineState:
    ml_results = state.get("ml_results", {})
    insights = state.get("insights", "")
    plan = generate_plan(insights, ml_results)
    state["plan"] = plan
    return state

import os
from langchain_groq import ChatGroq

def get_groq_client(model: str = "llama-3.1-8b-instant"):
    api_key = os.getenv("GROQ_API_KEY")
    return ChatGroq(api_key=api_key, model_name=model)

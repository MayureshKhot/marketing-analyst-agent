Each step is a “node” that updates a shared `PipelineState` object.This architecture makes the system:

- modular
- debuggable
- scalable
- easy to extend with new agents

---

### **🔹 2. Smart CSV Ingestion**

Automatically:

- loads CSV files
- infers schema
- formats datatypes
- handles null values
- validates required marketing columns

---

### **🔹 3. Automated EDA**

Computes core marketing KPIs:

- Total Spend, Total Revenue
- ROAS
- CTR, CPC, CPM
- Conversion Rate
- Cost Per Conversion
- Revenue Per Conversion

Also generates charts (Matplotlib):

- Spend vs Revenue
- CPC/CTR distributions
- Campaign-level metrics

---

### **🔹 4. Machine Learning Layer**

Includes baseline models such as:

- Performance classification
- Conversion prediction
- Feature importance
- Trend forecasting (optional)

Outputs a summary of actionable metrics for downstream agents.

---

### **🔹 5. LLM-Generated Insights (Groq)**

Using Groq LLMs, the system produces:

- performance summaries
- red flags
- optimization insights
- channel-level recommendations
- campaign strategies

Prompting is token-optimized for fast and cheap inference.

---

### **🔹 6. Action Plan Generator**

Builds an actionable **step-wise marketing plan**, including:

- Immediate optimization steps
- Experiments to run this month
- Long-term strategic shifts
- KPI targets and guardrails

Designed to feel like a real consulting deliverable.

---

### **🔹 7. Beautiful PDF Report**

The system generates a premium-quality PDF using:

- HTML template
- custom CSS design
- modern UI layout
- KPI cards
- insights & action steps
- visualizations inserted dynamically

Rendered using `pdfkit` + `wkhtmltopdf`.

---

## 🧠 Tech Stack

**Backend**

- Python
- FastAPI
- Pandas
- Scikit-learn
- Matplotlib
- Markdown → HTML converter

**AI / Orchestration**

- LangGraph
- Groq LLMs (Llama models)

**Report Generation**

- HTML/CSS Templates
- pdfkit
- wkhtmltopdf

---

## 📂 Project Structure

marketing-analytics-agent/

│

├── app/

│   ├── agents/

│   │   ├── ingestion_agent.py

│   │   ├── eda_agent.py

│   │   ├── ml_agent.py

│   │   ├── insight_agent.py

│   │   └── plan_agent.py

│   │

│   ├── services/

│   │   ├── langgraph_flow.py

│   │   └── groq_client.py

│   │

│   ├── templates/

│   │   └── report.html

│   │

│   ├── main.py

│   └── utils/

│       └── file_utils.py

│

├── reports/       # Generated PDFs

├── plots/         # Generated charts

├── .gitignore

├── README.md

└── requirements.txt

---

## ▶️ How It Works (High-Level)

1. **User uploads a CSV**
2. LangGraph starts the workflow
3. **Ingestion agent** loads & validates data
4. **EDA agent** computes KPIs + charts
5. **ML agent** runs predictive models
6. **Insight agent** (LLM) generates narrative insights
7. **Plan agent** (LLM) generates a full marketing strategy
8. **Report engine** produces a PDF with beautiful HTML styling
9. FastAPI returns the JSON or PDF to the user

---


## 🏁 Summary

This project demonstrates:

* practical agentic AI architecture
* clean workflow orchestration using LangGraph
* end-to-end marketing data analysis
* automated insight and strategy generation
* professional-grade PDF reporting

Built to showcase real-world AI engineering with a focus on clarity, modularity, and practical business value.


---
If you want, I can also generate:

✅ A project banner image  
✅ Flow diagrams (PNG/SVG)  
✅ Example screenshots  
✅ Example output JSON  
✅ Architecture diagram for the README  

Just tell me!
---

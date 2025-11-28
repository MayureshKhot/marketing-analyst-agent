import os
from datetime import datetime

import pdfkit
from jinja2 import Template
import markdown as md  # NEW

WKHTML_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"


def _format_kpis(kpis: dict) -> dict:
    """Round numbers and make them human friendly."""
    formatted = {}
    for k, v in kpis.items():
        if isinstance(v, (int, float)):
            # you can tweak this per metric later
            formatted[k] = round(v, 2)
        else:
            formatted[k] = v
    return formatted


def generate_html_report(kpis, insights, plan, charts, output_path="reports/report.pdf"):
    os.makedirs("reports", exist_ok=True)

    # 1) Format KPIs nicely
    kpis = _format_kpis(kpis)

    # 2) Convert insights & plan (markdown/plain text) -> HTML
    insights_html = md.markdown(insights)
    plan_html = md.markdown(plan)

    # 3) Make chart paths absolute so wkhtmltopdf can load them
    abs_charts = [os.path.abspath(p) for p in charts if p]

    # 4) Load the nice template
    template_path = os.path.join("app", "templates", "report.html")
    with open(template_path, "r", encoding="utf-8") as f:
        template = Template(f.read())

    html_content = template.render(
        date=datetime.now().strftime("%Y-%m-%d"),
        kpis=kpis,
        insights=insights_html,
        plan=plan_html,
        charts=abs_charts,
    )

    options = {
        "enable-local-file-access": "",  # flag option
        "page-size": "A4",
        "encoding": "UTF-8",
    }

    config = pdfkit.configuration(wkhtmltopdf=WKHTML_PATH)
    pdfkit.from_string(html_content, output_path, configuration=config, options=options)

    return output_path

from __future__ import annotations
import json, os
from typing import List, Dict, Any, Optional
from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_html(findings: List[Dict[str, Any]], out_dir: str, meta: Optional[Dict[str, Any]] = None) -> str:
    os.makedirs(out_dir, exist_ok=True)
    env = Environment(
        loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), "templates")),
        autoescape=select_autoescape()
    )
    template = env.get_template("report.html.j2")

    summary = {"high": 0, "medium": 0, "low": 0}
    for f in findings:
        sev = f.get("severity", "low").lower()
        if sev in summary:
            summary[sev] += 1

    html = template.render(findings=findings, summary=summary, meta=meta or {})
    out_path = os.path.join(out_dir, "report.html")
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(html)

    # also dump JSON (now includes meta)
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump({"meta": meta or {}, "summary": summary, "findings": findings}, f, indent=2)

    return out_path
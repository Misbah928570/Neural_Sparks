from flask import Blueprint, request, jsonify
from backend.models.granite_model import GraniteClient
from backend.utils.file_handler import read_any_file
from backend.utils.text_cleaner import clean_legal_text
from .auth import require_jwt
import json, re

risk_bp = Blueprint("risk", __name__)

SYSTEM_PROMPT = "You are a legal risk analyst. Return ONLY JSON with keys: risks (list)."

PROMPT_TEMPLATE = (
    "{system}\nIdentify risky clauses in the legal text. "
    "For each risk, provide title, severity (Low/Medium/High), and a short reason.\n\n"
    "Legal text:\n\"\"\"{text}\"\"\"\n\n"
    "Respond as strict JSON: {\"risks\": [{{title,severity,reason}}]}"
)

def _parse_json(s: str) -> dict:
    try:
        m = re.search(r"{[\s\S]*}", s)
        raw = m.group(0) if m else s
        return json.loads(raw)
    except Exception:
        return {"risks": []}

@risk_bp.post("/risk")
@require_jwt
def risk_only():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    text = read_any_file(f)
    text = clean_legal_text(text)[:12000]

    llm = GraniteClient()
    out = llm.generate(PROMPT_TEMPLATE.format(system=SYSTEM_PROMPT, text=text), max_new_tokens=400, temperature=0.2)
    data = _parse_json(out)
    return jsonify(data)

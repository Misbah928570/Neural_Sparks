from flask import Blueprint, request, jsonify
from backend.models.granite_model import GraniteClient
from backend.utils.file_handler import read_any_file
from backend.utils.text_cleaner import clean_legal_text
from .auth import require_jwt
import json, re

clause_bp = Blueprint("clause", __name__)

SYSTEM = (
    "You are ClauseWise, an AI legal assistant. Return ONLY JSON with keys: "
    "document_type, entities, clauses, risks."
)

PROMPT = (
    "{system}\n"
    "Task: Given legal text, perform (1) document type classification (NDA, Lease, Employment, Service Agreement, Other), "
    "(2) Named entities (PARTY, DATE, AMOUNT, OBLIGATION, TERM), "
    "(3) Clause extraction with simplified paraphrase, "
    "(4) Risk analysis with severity Low/Medium/High and a short reason.\n\n"
    "Legal text:\n\"\"\"{text}\"\"\"\n\n"
    "Respond as strict JSON: {\"document_type\": str, \"entities\": [{{label,text}}], \"clauses\": [{{original,simplified}}], \"risks\": [{{title,severity,reason}}]}"
)

def _first_json_block(s: str) -> dict:
    try:
        m = re.search(r"{[\s\S]*}", s)
        raw = m.group(0) if m else s
        return json.loads(raw)
    except Exception:
        return {"document_type": "Other", "entities": [], "clauses": [], "risks": []}


@clause_bp.post("/analyze")
@require_jwt
def analyze():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    text = read_any_file(f)
    text = clean_legal_text(text)[:12000]

    llm = GraniteClient()
    out = llm.generate(PROMPT.format(system=SYSTEM, text=text), max_new_tokens=700, temperature=0.2)
    data = _first_json_block(out)

    if not data.get("clauses"):
        sents = [s.strip() for s in re.split(r"(?<=\.)\s+", text) if len(s.strip()) > 20][:5]
        data["clauses"] = [{"original": s, "simplified": s[:140] + ("..." if len(s) > 140 else "")} for s in sents]
    if not data.get("entities"):
        data["entities"] = []
    if not data.get("risks"):
        data["risks"] = []

    dt = (data.get("document_type") or "Other").strip().title()
    if dt == "Nda":
        dt = "NDA"
    data["document_type"] = dt

    return jsonify(data)

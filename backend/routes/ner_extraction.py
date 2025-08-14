from flask import Blueprint, request, jsonify
from backend.models.granite_model import GraniteClient
from backend.utils.file_handler import read_any_file
from backend.utils.text_cleaner import clean_legal_text
from .auth import require_jwt

ner_bp = Blueprint("ner", __name__)

@ner_bp.post("/ner")
@require_jwt
def extract_entities():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    text = clean_legal_text(read_any_file(f))[:12000]

    client = GraniteClient()
    prompt = f"Extract all named entities (PARTY, DATE, AMOUNT, OBLIGATION, TERM) from:\n{text}"
    entities = client.generate(prompt, max_new_tokens=400)
    return jsonify({"entities": entities})

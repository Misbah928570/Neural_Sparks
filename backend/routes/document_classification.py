from flask import Blueprint, request, jsonify
from backend.models.granite_model import GraniteClient
from backend.utils.file_handler import read_any_file
from backend.utils.text_cleaner import clean_legal_text
from .auth import require_jwt

doc_class_bp = Blueprint("doc_class", __name__)

@doc_class_bp.post("/classify")
@require_jwt
def classify_document():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    text = clean_legal_text(read_any_file(f))[:12000]

    client = GraniteClient()
    prompt = f"Classify the following legal document into NDA, Lease, Employment, Service Agreement, Other:\n{text}"
    doc_type = client.generate(prompt, max_new_tokens=200)
    return jsonify({"document_type": doc_type.strip()})

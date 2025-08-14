# backend/routes/clause_simplification.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict
import json

from backend.models.granite_model import GraniteClient
from backend.utils.file_handler import read_any_file
from backend.utils.text_cleaner import normalize_spaces

router = APIRouter()
MODEL_PROMPT = """You are ClauseWise. Simplify the following legal text into clear, plain-language points.
Return JSON: {"simplified":"..."}.

Legal text:
\"\"\"{text}\"\"\""""

@router.post("/simplify-clause")
async def simplify_clause(file: UploadFile = File(...)) -> Dict:
    """
    Upload a file (PDF/DOCX/TXT) and return a simplified version of the main clauses.
    """
    try:
        raw = await file.read()
        text = read_any_file(file) if hasattr(file, "filename") else raw.decode("utf-8", errors="ignore")
        text = normalize_spaces(text)[:12000]
        if not text:
            raise HTTPException(status_code=400, detail="No readable text in file.")

        client = GraniteClient()
        prompt = MODEL_PROMPT.format(text=text)
        out = client.generate(prompt, max_new_tokens=700, temperature=0.2)

        # Try to parse JSON
        try:
            parsed = json.loads(out)
            simplified = parsed.get("simplified") or parsed.get("summary") or parsed
            return {"simplified_text": simplified}
        except Exception:
            # Fallback: return raw generated text as simplified_text
            return {"simplified_text": out.strip()}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# backend/routes/clause_extraction.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Dict, List
import json, re

from ..models.granite_model import GraniteClient
from ..utils.file_handler import read_any_file
from ..utils.text_cleaner import normalize_spaces

router = APIRouter()
PROMPT = """You are ClauseWise. Split the following legal document into key clauses.
Return JSON: {{"clauses":[{{"original":"...","simplified":"..."}}]}}.

Text:
\"\"\"{text}\"\"\""""

def naive_split(text: str) -> List[str]:
    # Try to split on numbered lists, section markers or long sentence groups
    parts = re.split(r'\n\s*\d+[\.\)]\s+|\n\s*\(\w+\)\s+|(?<=\.)\s{2,}|\n-{2,}\n', text)
    cleaned = [p.strip() for p in parts if len(p.strip()) > 30]
    if not cleaned:
        # final fallback: sentence-based chunks
        sents = re.split(r'(?<=\.)\s+', text)
        chunks = []
        for i in range(0, len(sents), 3):
            chunk = " ".join(sents[i:i+3]).strip()
            if len(chunk) > 30:
                chunks.append(chunk)
        return chunks[:60]
    return cleaned[:60]

@router.post("/clauses")
async def clauses_route(file: UploadFile = File(...)) -> Dict:
    try:
        text = read_any_file(file)
        text = normalize_spaces(text)[:20000]
        if not text:
            raise HTTPException(status_code=400, detail="No readable text.")

        client = GraniteClient()
        out = client.generate(PROMPT.format(text=text), max_new_tokens=1000, temperature=0.15)

        try:
            parsed = json.loads(out)
            clauses = parsed.get("clauses") or []
            if clauses:
                return {"clauses": clauses, "count": len(clauses)}
        except Exception:
            pass

        # fallback: naive split + try to simplify a few clauses with Granite
        raw_clauses = naive_split(text)
        simplified = []
        for c in raw_clauses[:12]:
            try:
                s_prompt = f"Simplify the clause into plain language (one to three sentences):\n\n{c}"
                s_out = client.generate(s_prompt, max_new_tokens=200, temperature=0.15)
                simplified.append({"original": c, "simplified": s_out.strip()})
            except Exception:
                simplified.append({"original": c, "simplified": c[:180] + ("..." if len(c) > 180 else "")})
        return {"clauses": simplified, "count": len(raw_clauses)}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

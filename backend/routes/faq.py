# backend/routes/faq.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/faq")
async def get_faq():
    faqs = [
        {
            "question": "What is ClauseWise?",
            "answer": "ClauseWise is an AI-powered legal document analyzer that simplifies, decodes, and classifies legal texts."
        },
        {
            "question": "Which file formats are supported?",
            "answer": "PDF, DOCX, and TXT."
        },
        {
            "question": "Do you store my documents?",
            "answer": "By default, uploads are processed in-memory and not stored. Production options can include encrypted storage with consent."
        },
        {
            "question": "Is ClauseWise legal advice?",
            "answer": "No. ClauseWise provides AI-assisted analysis; consult a lawyer for binding legal decisions."
        }
    ]
    return {"faq": faqs}

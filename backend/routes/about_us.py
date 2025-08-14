# backend/routes/about_us.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/about")
async def get_about():
    return {
        "about": {
            "name": "ClauseWise",
            "description": "ClauseWise automates clause simplification, extraction, classification, and risk detection using IBM Granite on Hugging Face.",
            "mission": "To make legal documents transparent and easy to understand.",
            "tech_stack": ["Python", "IBM Granite (Hugging Face)", "Streamlit", "FastAPI"],
            "contact": {"email": "support@clausewise.example", "website": "https://clausewise.example"}
        }
    }

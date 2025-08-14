import streamlit as st

TRANSLATIONS = {
    "en": {
        "app_name": "ClauseWise",
        "tagline": "AI-powered Legal Document Analyzer",
        "login": "Login",
        "signup": "Signup",
        "email": "Email",
        "password": "Password",
        "upload": "Upload a legal document (PDF/DOCX/TXT)",
        "analyze": "Analyze",
        "clause": "Clause Simplification",
        "risk": "Risk Analyzer",
        "classify": "Document Classification",
        "faq": "FAQ",
        "about": "About Us",
        "logout": "Logout",
        "need_login": "Please login first.",
        "choose_lang": "Language",
        "doc_type": "Document Type",
        "entities": "Named Entities",
        "clauses": "Clauses",
        "risks": "Risks",
    },
    "hi": {
        "app_name": "क्लॉज़वाइज़",
        "tagline": "एआई-संचालित कानूनी दस्तावेज़ विश्लेषक",
        "login": "लॉगिन",
        "signup": "साइन अप",
        "email": "ईमेल",
        "password": "पासवर्ड",
        "upload": "कानूनी दस्तावेज़ अपलोड करें (PDF/DOCX/TXT)",
        "analyze": "विश्लेषण करें",
        "clause": "धारा सरलीकरण",
        "risk": "जोखिम विश्लेषक",
        "classify": "दस्तावेज़ वर्गीकरण",
        "faq": "सामान्य प्रश्न",
        "about": "हमारे बारे में",
        "logout": "लॉग आउट",
        "need_login": "कृपया पहले लॉगिन करें।",
        "choose_lang": "भाषा",
        "doc_type": "दस्तावेज़ प्रकार",
        "entities": "नामित संस्थाएँ",
        "clauses": "धाराएँ",
        "risks": "जोखिम",
    },
    "ur": {
        "app_name": "کلاز وائز",
        "tagline": "اے آئی سے چلنے والا قانونی دستاویز تجزیہ کار",
        "login": "لاگ اِن",
        "signup": "سائن اَپ",
        "email": "ای میل",
        "password": "پاس ورڈ",
        "upload": "قانونی دستاویز اپلوڈ کریں (PDF/DOCX/TXT)",
        "analyze": "تجزیہ کریں",
        "clause": "شق کی سادہ تشریح",
        "risk": "خطرہ تجزیہ کار",
        "classify": "دستاویز کی درجہ بندی",
        "faq": "عمومی سوالات",
        "about": "ہمارے بارے میں",
        "logout": "لاگ آؤٹ",
        "need_login": "براہِ کرم پہلے لاگ اِن کریں۔",
        "choose_lang": "زبان",
        "doc_type": "دستاویز کی قسم",
        "entities": "نامزد ادارے",
        "clauses": "شقوق",
        "risks": "خطرات",
    },
}

LANG_OPTIONS = {"English": "en", "Hindi": "hi", "Urdu": "ur"}


def get_lang():
    if "lang" not in st.session_state:
        st.session_state.lang = "en"
    return st.session_state.lang


def set_lang_from_label(label: str):
    st.session_state.lang = LANG_OPTIONS.get(label, "en")


def t(key: str) -> str:
    lang = get_lang()
    return TRANSLATIONS.get(lang, TRANSLATIONS["en"]).get(key, key)
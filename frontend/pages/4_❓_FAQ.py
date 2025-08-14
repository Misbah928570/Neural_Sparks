import streamlit as st
from googletrans import Translator
import base64

translator = Translator()

# Background image
def set_bg():
    with open("assets/background.jpg", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/jpeg;base64,{b64}");
            background-size: cover;
            background-position: center;
        }}
        .faq-box {{
            background: rgba(255,255,255,0.85);
            padding: 15px;
            border-radius: 10px;
            margin-bottom: 15px;
            transition: transform 0.2s ease;
        }}
        .faq-box:hover {{
            transform: scale(1.02);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# Multilingual
def t(text, lang):
    return translator.translate(text, dest=lang).text if lang != "en" else text

lang = st.sidebar.selectbox("🌍 Language", ["en", "hi", "ur", "fr", "es"])

st.title(t("📜 Frequently Asked Questions", lang))

faqs = [
    {
        "q": "What is ClauseWise?",
        "a": "ClauseWise is an AI tool for simplifying, classifying, and analyzing legal documents."
    },
    {
        "q": "Which file formats are supported?",
        "a": "You can upload PDF, DOCX, or TXT files."
    },
    {
        "q": "Does ClauseWise replace lawyers?",
        "a": "No. It assists lawyers and businesses but does not provide legal advice."
    },
    {
        "q": "Is my data secure?",
        "a": "Yes. Uploaded files are processed securely and deleted after analysis."
    }
]

for item in faqs:
    with st.container():
        st.markdown(f"<div class='faq-box'><b>{t(item['q'], lang)}</b><br>{t(item['a'], lang)}</div>", unsafe_allow_html=True)

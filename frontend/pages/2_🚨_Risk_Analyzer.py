import streamlit as st
from googletrans import Translator
import base64

# Translator setup
translator = Translator()

# Background image
def set_bg():
    with open("assets/court_scale.png", "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode()
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
            background-position: center;
        }}
        .stButton>button:hover {{
            background-color: #ffcc00 !important;
            color: black !important;
            transform: scale(1.05);
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

set_bg()

# Multilingual function
def t(text, lang):
    return translator.translate(text, dest=lang).text if lang != "en" else text

# Sidebar language select
lang = st.sidebar.selectbox("🌍 Language", ["en", "hi", "ur", "fr", "es"])

st.title(t("⚖ Risk Analyzer", lang))
st.write(t("Upload a legal document to automatically detect potential risks and obligations.", lang))

uploaded_file = st.file_uploader(t("Choose a file (PDF/DOCX/TXT)", lang), type=["pdf", "docx", "txt"])

if uploaded_file:
    st.success(t("File uploaded successfully!", lang))
    if st.button(t("🔍 Analyze Risks", lang)):
        with st.spinner(t("Analyzing document risks using AI...", lang)):
            # Placeholder API call
            risks = [
                "Confidentiality clause may be vague.",
                "Payment terms not clearly defined.",
                "Termination clause heavily favors one party."
            ]
            st.subheader(t("Identified Risks:", lang))
            for r in risks:
                st.warning(t(r, lang))

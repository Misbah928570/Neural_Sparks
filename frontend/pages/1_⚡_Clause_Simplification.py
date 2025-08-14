import streamlit as st
import requests
import os
from dotenv import load_dotenv
from lib.i18n import t, get_lang
from lib.ui import apply_css, set_bg, lottie

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title=t('clause'), page_icon="⚡", layout="wide")
apply_css()
set_bg("bg_clause.jpg")

st.title(f"⚡ {t('clause')}")

if "token" not in st.session_state:
    st.session_state.token = None

with st.container():
    st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
    file = st.file_uploader(t("upload"), type=["pdf","docx","txt"], key="clause_file")
    st.markdown("</div>", unsafe_allow_html=True)

    if file and st.button(t("analyze")):
        files = {"file": (file.name, file.getvalue(), file.type)}
        headers = {"Authorization": f"Bearer {st.session_state.token}"} if st.session_state.token else {}
        url = f"{API_BASE}/analyze"
        with st.spinner("Analyzing with Granite …"):
            r = requests.post(url, headers=headers, files=files, timeout=180)
        if r.ok:
            out = r.json()
            st.subheader(t("doc_type"))
            st.success(out.get("document_type", ""))

            st.subheader(t("clauses"))
            for c in out.get("clauses", []):
                st.markdown(f"**Simplified:** {c.get('simplified','')}")
               
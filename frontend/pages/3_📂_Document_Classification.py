# frontend/pages/document_classification.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os

from lib.i18n import t
from lib.ui import apply_css, set_bg, lottie

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title=f"📂 {t('classify')}", page_icon="📂", layout="wide")
apply_css()
set_bg("bg_classify.jpg")

st.title(f"📂 {t('classify')}")
st.markdown("Automatically detect the type of the uploaded legal document (NDA, Lease, Employment, Service Agreement, etc.).")

# optional animation
lottie("anim_classify.json", height=200, key="classify_anim")

if "token" not in st.session_state:
    st.session_state.token = None

st.markdown("<div class='upload-box'>", unsafe_allow_html=True)
file = st.file_uploader(t("upload"), type=["pdf", "docx", "txt"], key="classify_file")
st.markdown("</div>", unsafe_allow_html=True)

if file and st.button(t("analyze"), key="run_classify"):
    headers = {}
    if st.session_state.get("token"):
        headers["Authorization"] = f"Bearer {st.session_state.token}"

    files = {"file": (file.name, file.getvalue(), file.type)}
    url = f"{API_BASE}/classify"

    try:
        with st.spinner("Classifying document..."):
            resp = requests.post(url, headers=headers, files=files, timeout=120)
        if resp.ok:
            out = resp.json()
            # backend might return {"document_type": "..."} or {"classification": {...}}
            doc_type = out.get("document_type") or (out.get("classification") or {}).get("category") or out.get("classification") or out
            if isinstance(doc_type, dict):
                # try known keys
                label = doc_type.get("document_type") or doc_type.get("category") or str(doc_type)
                st.success(f"Document Type: {label}")
                conf = doc_type.get("confidence_score")
                if conf:
                    st.write(f"Confidence: {conf}")
            else:
                st.success(f"Document Type: {doc_type}")
        else:
            try:
                st.error(resp.json())
            except Exception:
                st.error(resp.text)
    except requests.exceptions.RequestException as e:
        st.error(f"Request failed: {e}")

with st.sidebar:
    st.header("Auth")
    email = st.text_input("Email", key="auth_email_cls")
    pw = st.text_input("Password", type="password", key="auth_pw_cls")
    c1, c2 = st.columns(2)
    if c1.button("Signup"):
        try:
            rr = requests.post(f"{API_BASE}/signup", json={"email": email, "password": pw}, timeout=30)
            st.write(rr.json())
        except Exception as e:
            st.error(str(e))
    if c2.button("Login"):
        try:
            rr = requests.post(f"{API_BASE}/login", json={"email": email, "password": pw}, timeout=30)
            if rr.ok:
                st.session_state.token = rr.json().get("token")
                st.success("Logged in!")
            else:
                st.error(rr.json())
        except Exception as e:
            st.error(str(e))

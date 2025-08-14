# frontend/pages/about_us.py
import streamlit as st
import requests
from dotenv import load_dotenv
import os

from lib.i18n import t
from lib.ui import apply_css, set_bg, lottie

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title=f"ℹ️ {t('about')}", page_icon="ℹ️", layout="wide")
apply_css()
set_bg("bg_about.jpg")

st.title(f"ℹ️ {t('about')}")
st.markdown("Learn about ClauseWise — mission, tech stack, and contacts.")

# optional animation
lottie("anim_classify.json", height=180, key="about_anim")

# try to fetch from backend for dynamic about content
about_info = {}
try:
    with st.spinner("Loading..."):
        resp = requests.get(f"{API_BASE}/about", timeout=8)
    if resp.ok:
        about_info = resp.json().get("about", {})
except Exception:
    about_info = {}

if about_info:
    st.subheader(about_info.get("name", "ClauseWise"))
    st.write(about_info.get("description", ""))
    st.markdown(f"**Mission:** {about_info.get('mission','')}")
    st.markdown("**Tech stack:** " + ", ".join(about_info.get("tech_stack", ["Python","IBM Granite","Streamlit","HuggingFace"])))
    contact = about_info.get("contact", {})
    if contact:
        st.markdown(f"**Contact:** {contact.get('email','')} — {contact.get('website','')}")
else:
    st.markdown(
        """
**ClauseWise** simplifies and analyzes legal documents using **Python, IBM Watson/Granite, Streamlit, and HuggingFace**.

**Mission:** To make legal documents transparent and understandable for everyone.

**Tech stack:** Python, IBM Watson, Granite, Streamlit, HuggingFace
        """
    )

st.markdown("---")
st.write("Built with ❤️ — ClauseWise Team")

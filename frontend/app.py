import streamlit as st
import requests
from dotenv import load_dotenv
import os
from frontend.lib.i18n import t, TRANSLATIONS, LANG_OPTIONS, get_lang, set_lang_from_label
from frontend.lib.ui import apply_css, set_bg, lottie, topbar

load_dotenv()
API_BASE = os.getenv("API_BASE", "http://localhost:8000/api")

st.set_page_config(page_title="ClauseWise", page_icon="⚖️", layout="wide")
apply_css()
set_bg("bg_landing.jpg")

# --- Language state from topbar ---
label_default = {v:k for k,v in LANG_OPTIONS.items()}[get_lang()]
topbar(label_default)  # shows logo + language dropdown
if "lang_selector" in st.session_state:
    set_lang_from_label(st.session_state.lang_selector)

# --- Hero ---
st.markdown(f"<h1 class='hero-title'>{t('app_name')}</h1>", unsafe_allow_html=True)
st.markdown(f"<p class='hero-sub'>{t('tagline')}</p>", unsafe_allow_html=True)

colA, colB, colC = st.columns(3)
with colA:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### ⚡ {t('clause')}")
    st.write("Simplify complex clauses to plain language.")
    st.page_link("pages/1_⚡_Clause_Simplification.py", label=t('clause'), icon="⚡")
    st.markdown("</div>", unsafe_allow_html=True)
with colB:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### 🚨 {t('risk')}")
    st.write("Identify high‑risk provisions with severity & reasons.")
    st.page_link("pages/2_🚨_Risk_Analyzer.py", label=t('risk'), icon="🚨")
    st.markdown("</div>", unsafe_allow_html=True)
with colC:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### 📂 {t('classify')}")
    st.write("Auto-detect NDA, Lease, Employment, or Other.")
    st.page_link("pages/3_📂_Document_Classification.py", label=t('classify'), icon="📂")
    st.markdown("</div>", unsafe_allow_html=True)

# Secondary row
colD, colE = st.columns(2)
with colD:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### ❓ {t('faq')}")
    st.page_link("pages/4_❓_FAQ.py", label=t('faq'), icon="❓")
    st.markdown("</div>", unsafe_allow_html=True)
with colE:
    st.markdown("<div class='card'>", unsafe_allow_html=True)
    st.markdown(f"### ℹ️ {t('about')}")
    st.page_link("pages/5_ℹ️_About_Us.py", label=t('about'), icon="ℹ️")
    st.markdown("</div>", unsafe_allow_html=True)

st.caption("Tip: set API_BASE in .env to point to your Flask backend.")
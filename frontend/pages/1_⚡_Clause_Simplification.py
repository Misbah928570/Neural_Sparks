import streamlit as st
import requests
from pathlib import Path
import time
import base64
# --- Path Configuration ---
ASSETS_DIR = Path(__file__).parent.parent / "assets"

# --- Background Setup ---
def set_bg():
    bg_path = ASSETS_DIR / "images" / "bg_clause.jpg"
    try:
        with open(bg_path, "rb") as f:
            data = f.read()
        b64 = base64.b64encode(data).decode()
        st.markdown(f"""
        <style>
        .stApp {{
            background-image: url("data:image/png;base64,{b64}");
            background-size: cover;
        }}
        </style>
        """, unsafe_allow_html=True)
    except:
        st.markdown("""<style>.stApp { background-color: #f0f2f6; }</style>""", unsafe_allow_html=True)

set_bg()

# --- Document Analysis Function ---
def analyze_document(file):
    API_URL = "http://localhost:8000/api/analyze"
    
    with st.spinner("🔍 Analyzing with IBM Granite..."):
        try:
            response = requests.post(
                API_URL,
                files={"file": file},
                timeout=120
            )
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            st.error(f"❌ Analysis failed: {str(e)}")
            return None

# --- Main UI ---
st.title("⚖️ Legal Clause Analyzer")
uploaded_file = st.file_uploader("Upload Legal Document (PDF/DOCX/TXT)", type=["pdf", "docx", "txt"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")
    
    if st.button("Analyze with IBM Granite", type="primary"):
        analysis = analyze_document(uploaded_file)
        
        if analysis and analysis.get("status") == "success":
            st.subheader("Analysis Results")
            for item in analysis["result"]["analysis"]:
                with st.expander(f"**{item['type']}** (Risk: {item['risk']})"):
                    st.write(f"**Original Clause:**\n{item['clause']}")
                    st.write(f"**Issues Found:**\n{', '.join(item['issues'])}")
                    st.write(f"**Suggested Revision:**\n{item['suggestion']}")
        else:
            st.warning("No analysis results returned")
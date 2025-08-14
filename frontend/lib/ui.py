import streamlit as st
from pathlib import Path
from streamlit_lottie import st_lottie
import json
from typing import Optional, Union

# Constants
ASSETS_DIR = Path(__file__).parent.parent / "assets"  # Adjusted to frontend/assets
CSS_DIR = ASSETS_DIR / "css"
LOTTIE_DIR = ASSETS_DIR / "lottie"
IMAGES_DIR = ASSETS_DIR / "images"

def apply_css():
    # Correct path resolution (goes up from lib/ to frontend/, then into assets/css)
    css_path = Path(__file__).parent.parent / "assets" / "css" / "styles.css"
    
    # Debugging output
    print(f"🔍 Looking for CSS at: {css_path}")
    print(f"📁 Path exists: {css_path.exists()}")
    
    try:
        css = css_path.read_text(encoding="utf-8")
        st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)
    except FileNotFoundError:
        st.error(f"""
        ❌ CSS file not found at: 
        {css_path}
        Please ensure:
        1. The file exists
        2. The path is correct
        3. File permissions allow reading
        """)
        # Fallback minimal styles
        st.markdown("""
        <style>
        body { font-family: Arial; }
        </style>
        """, unsafe_allow_html=True)

def set_bg(image_name: str):
    """Set background image from assets/images"""
    bg_path = IMAGES_DIR / image_name
    if not bg_path.exists():
        st.error(f"Background image not found: {bg_path}")
        return
    
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: url('{bg_path}');
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
            background-repeat: no-repeat;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

def lottie(file_name: str, height: int = 260, key: Optional[str] = None):
    """Load and display Lottie animation"""
    lottie_path = LOTTIE_DIR / file_name
    if not lottie_path.exists():
        st.warning(f"Lottie file not found: {lottie_path}")
        return
    
    try:
        with open(lottie_path, "r", encoding="utf-8") as f:
            animation = json.load(f)
        st_lottie(animation, height=height, key=key or file_name)
    except Exception as e:
        st.error(f"Failed to load Lottie animation: {e}")

def topbar(lang_label: str = "English"):
    """Create top navigation bar with logo and language selector"""
    st.markdown(
        """
        <style>
        .topbar {
            position: fixed;
            top: 0;
            width: 100%;
            z-index: 100;
            background-color: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            padding: 10px 0;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    
    with st.container():
        col1, col2, col3 = st.columns([1, 5, 2])
        with col1:
            logo_path = IMAGES_DIR / "logo.png"
            if logo_path.exists():
                st.image(str(logo_path), width=90)
            else:
                st.error("Logo image not found")
        with col3:
            selected_lang = st.selectbox(
                " ",
                ["English", "Hindi", "Urdu"],
                index=["English", "Hindi", "Urdu"].index(lang_label),
                key="lang_selector"
            )
            return selected_lang
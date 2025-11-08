# pages/home.py
import os
import sys
import streamlit as st



# --- Add root path for imports ---
ROOT = os.path.dirname(os.path.dirname(__file__))  # Go up to project root
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

# --- Import custom components ---

from components.NavBar.navbar import navbar
from components.Hero import (
    custom_css_injection,
    render_brand_header,
    render_hero_section,
    render_cta_banner
)
from components.features import load_feature_section

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="SmartBricks | Home",
    page_icon="🏠",
    layout="wide"
)

# ---------------- GLOBAL CSS ----------------
st.markdown("""
    <style>
        * {
            font-family: 'Poppins', sans-serif;
        }
        .main {
            background-color: #f7f9fb;
        }
        section {
            margin-top: 3rem;
            margin-bottom: 3rem;
        }
        h2, h3 {
            text-align: center;
            color: #003366;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- INITIAL SESSION STATE ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- NAVBAR ----------------
navbar()  # your custom navbar (includes Login/Signup buttons)

# ---------------- HERO SECTION ----------------
custom_css_injection()
render_brand_header()
render_hero_section()
render_cta_banner()

# ---------------- FEATURES SECTION ----------------
load_feature_section()

# ---------------- FOOTER (already included in features) ----------------
st.markdown("<br><br>", unsafe_allow_html=True)

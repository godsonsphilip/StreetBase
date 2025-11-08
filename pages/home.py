# pages/your_page.py
import os, sys
from turtle import st
ROOT = os.path.dirname(os.path.dirname(__file__))  # .. up to project root
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from components.NavBar.home import load_navbar
from components.Hero import load_hero_section
from components.simple_app import load_model_section
from components.features import load_footer_section

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

# ---------------- NAVBAR ----------------
load_navbar()  # your custom navbar (includes Login/Signup buttons)

# ---------------- HERO SECTION ----------------
load_hero_section()

# ---------------- MODEL SECTION ----------------
load_model_section()

# ---------------- FOOTER SECTION ----------------
load_footer_section()

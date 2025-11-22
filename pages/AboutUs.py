# ---------------- TOP IMPORT FIXES ----------------
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# ---------------------------------------------------

import streamlit as st
import qrcode
import io


from components.NavBar.navbar import navbar
from backend.api.email_api import send_contact_email


def load_about_us_page():

    st.set_page_config(page_title="StreetBase", layout="wide")

    # ---------------- CSS ----------------
    st.markdown("""
    <style>
    #MainMenu, header, footer {visibility: hidden;}
    body, .block-container {
        background-color: #FFFDF2;
        color: #2b2b2b;
        font-family: 'Segoe UI', sans-serif;
        max-width: 95%;
        margin: auto;
    }
    .title {
        text-align: center;
        font-size: 3rem;
        font-weight: 800;
        color: #004D00;
    }
    .subtitle {
        text-align: center;
        font-size: 1.25rem;
        color: #555;
        margin-bottom: 2rem;
    }
    .section-title {
        text-align: center;
        font-size: 2rem;
        font-weight: 700;
        color: #004D00;
        margin-top: 3rem;
        margin-bottom: 1rem;
    }
    .card {
        background: #FFFFFF;
        border-radius: 18px;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        padding: 25px;
        text-align: center;
        border-top: 5px solid #E2725B;
    }
    .card:hover {
        transform: translateY(-6px);
        box-shadow: 0 6px 22px rgba(226,114,91,0.3);
    }
    div[data-testid="stForm"] {
        background-color: #FFFDF2;
        padding: 35px 40px;
        border-radius: 18px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.08);
        max-width: 800px;
        margin: auto;
        border: 1px solid #E2E2E2;
    }
    .stTextInput > div > div > input,
    .stTextArea textarea {
        border: 2px solid #004D00 !important;
        border-radius: 10px !important;
        padding: 10px !important;
        font-size: 1rem !important;
        background-color: #FFFFFF !important;
        color: #000000 !important;
    }
    .stButton button {
        background-color: #F5B895 !important;
        color: #FFFFFF !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        padding: 10px 24px !important;
    }
    .stButton button:hover {
        background-color: #E2725B !important;
        transform: scale(1.05);
    }
    .contact-success {
        text-align: center;
        color: #004D00;
        font-weight: 600;
        background-color: #EAF5EA;
        border-radius: 10px;
        padding: 12px;
        margin-top: 15px;
    }
    .footer {
        text-align: center;
        color: #004D00;
        background-color: #EDE9D5;
        padding: 1.5rem 0;
        margin-top: 3rem;
        border-top: 2px solid #E2725B;
    }
     hr {
        border: none;
        height: 2px;
        background-color: #E2725B;
        margin: 3rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

    # ---------------- NAVBAR ----------------
    navbar()

    # ---------------- HEADER ----------------
    st.markdown("<h1 class='title'>🏠 StreetBase</h1>", unsafe_allow_html=True)
    st.markdown("<p class='subtitle'>Building Smarter, Sustainable Homes with Data Intelligence</p>",
                unsafe_allow_html=True)

    st.write("""
    StreetBase is an AI-powered real estate evaluation platform using Machine Learning
    to predict housing prices and promote sustainable living choices.
    """)

    st.divider()

    # ---------------- TEAM SECTION ----------------
    st.markdown("<h2 class='section-title'>👥 Meet Our Team</h2>", unsafe_allow_html=True)
    cols = st.columns(4)

    for i, col in enumerate(cols, start=1):
        with col:
            st.markdown(f"""
            <div class="card">
                <h3>Teammate {i}</h3>
                <p>Role {i}</p>
                <p>🌐 <a href="#" style="color:#E2725B;text-decoration:none;">LinkedIn</a> |
                   💻 <a href="#" style="color:#E2725B;text-decoration:none;">GitHub</a></p>
            </div>
            """, unsafe_allow_html=True)

    st.divider()

    # ---------------- CONTACT FORM ----------------
    st.markdown("<h2 class='section-title'>📬 Contact Us</h2>", unsafe_allow_html=True)

    with st.form("contact_form"):
        name = st.text_input("Your Name", placeholder="Enter your full name")
        email = st.text_input("Your Email", placeholder="Enter your email address")
        message = st.text_area("Your Message", placeholder="Type your message here...")

        submitted = st.form_submit_button("Send Message")

        if submitted:
            if not name or not email or not message:
                st.error("⚠️ Please fill out all fields.")
            else:
                result = send_contact_email(name, email, message)

                if result["status"]:
                    st.markdown(
                        '<div class="contact-success">✅ Thank you! We will reach out soon.</div>',
                        unsafe_allow_html=True
                    )
                else:
                    st.error(f"❌ Email failed: {result['error']}")

    st.divider()

    # ---------------- FUTURE SCOPE ----------------
    st.markdown("<h2 class='section-title'>🚀 Future Scope</h2>", unsafe_allow_html=True)

    st.markdown("""
    - 🌍 Live Real Estate API Integration  
    - ☁️ Cloud Deployment (AWS, GCP)  
    - 🧠 Explainable AI (SHAP, LIME)  
    - 📊 Interactive analytics dashboard  
    """)

    st.divider()

    # ---------------- CONNECT WITH US ----------------
    st.markdown("<h2 class='section-title'>🌐 Connect With Us</h2>", unsafe_allow_html=True)

    st.write("📧 streetbase5@gmail.com")
    st.write("🌍 www.streetbase.ai")

    try:
        qr = qrcode.make("https://github.com/your-project-repo")
        buf = io.BytesIO()
        qr.save(buf, format="PNG")
        st.image(buf.getvalue(), width=130)
    except:
        st.write("QR Code could not be generated")

    # ---------------- FOOTER ----------------
    st.markdown("""
    <div class="footer">
        <b>StreetBase</b> © 2025 — Innovating Real Estate Intelligence with AI
    </div>
    """, unsafe_allow_html=True)

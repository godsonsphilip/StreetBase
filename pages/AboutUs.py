# --- put these 5 lines at the very top ---
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]  # points to .../SmartBricks
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# -----------------------------------------

from components.NavBar.navbar import navbar
import qrcode
import io
import streamlit as st # <-- Move this line to the top

# -----------------------------------------------------------
# PAGE CONFIG
# -----------------------------------------------------------
st.set_page_config(page_title="StreetBase", layout="wide")

# ... (rest of your code remains the same) ...

# -----------------------------------------------------------
# CUSTOM CSS
# -----------------------------------------------------------
st.markdown("""
<style>
/* --------------------- GLOBAL --------------------- */
#MainMenu, header, footer {visibility: hidden;}
body, .block-container {
    background-color: #FFFDF2; /* Cream background */
    color: #2b2b2b;
    font-family: 'Segoe UI', sans-serif;
    padding-top: 1rem;
    max-width: 95%;
    margin: auto;
}

/* Titles */
.title {
    text-align: center;
    font-size: 3rem;
    font-weight: 800;
    color: #004D00; /* Forest Green */
}
.subtitle {
    text-align: center;
    font-size: 1.25rem;
    color: #555;
    margin-bottom: 2rem;
}

/* Section Headings */
.section-title {
    text-align: center;
    font-size: 2rem;
    font-weight: 700;
    color: #004D00;
    margin-top: 3rem;
    margin-bottom: 1rem;
}

/* --------------------- TEAM CARDS --------------------- */
.card {
    background: #FFFFFF;
    border-radius: 18px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    padding: 25px;
    text-align: center;
    transition: all 0.3s ease;
    border-top: 5px solid #E2725B; /* Terracotta accent */
}
.card:hover {
    transform: translateY(-6px);
    box-shadow: 0 6px 22px rgba(226,114,91,0.3);
}
.card h3 {
    color: #004D00;
    font-weight: 700;
    margin-bottom: 6px;
}
.card p {
    color: #444;
    font-size: 0.95rem;
}

/* --------------------- CONTACT FORM --------------------- */
.contact-container {
    background-color: #FFFDF2;
    padding: 35px 40px;
    border-radius: 18px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    max-width: 800px;
    margin: auto;
    border: 1px solid #E2E2E2;
}

/* Input fields */
.stTextInput > div > div > input,
.stTextArea textarea {
    border: 2px solid #004D00 !important;
    border-radius: 10px !important;
    padding: 10px !important;
    font-size: 1rem !important;
    background-color: #FFFFFF !important;
    color: #000000 !important;
}

/* Labels */
label, .stTextInput label, .stTextArea label {
    color: #000000 !important; /* Black labels */
    font-weight: 600 !important;
    font-size: 1rem !important;
}

/* Button */
.stButton button {
    background-color: #F5B895 !important; /* pastel terracotta */
    color: #FFFFFF !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    font-size: 1rem !important;
    padding: 10px 24px !important;
    border: none !important;
    transition: all 0.3s ease-in-out !important;
    box-shadow: 0 3px 8px rgba(0,0,0,0.2);
}
.stButton button:hover {
    background-color: #E2725B !important; /* deeper terracotta */
    color: #FFFFFF !important;
    transform: scale(1.05);
    box-shadow: 0 6px 15px rgba(0,0,0,0.25);
}
.stButton button:disabled {
    background-color: #F5B895 !important;
    color: #FFFFFF !important;
    opacity: 0.9 !important;
}

/* Success message */
.contact-success {
    text-align: center;
    color: #004D00;
    font-weight: 600;
    background-color: #EAF5EA;
    border-radius: 10px;
    padding: 12px;
    margin-top: 15px;
}

/* --------------------- FOOTER --------------------- */
.footer {
    text-align: center;
    color: #004D00;
    font-size: 0.95rem;
    background-color: #EDE9D5;
    border-top: 2px solid #E2725B;
    padding: 1.5rem 0;
    margin-top: 3rem;
}
.footer b { color: #004D00; }

/* Divider Styling */
hr {
    border: none;
    height: 2px;
    background-color: #E2725B;
    margin: 3rem 0;
}
</style>
""", unsafe_allow_html=True)

navbar()  # your custom navbar (includes Login/Signup buttons)

# -----------------------------------------------------------
# HEADER
# -----------------------------------------------------------
st.markdown("<h1 class='title'>🏠 StreetBase</h1>", unsafe_allow_html=True)
st.markdown("<p class='subtitle'>Building Smarter, Sustainable Homes with Data Intelligence</p>", unsafe_allow_html=True)

st.write("""
StreetBase is an AI-powered real estate evaluation platform that empowers users with transparent, 
data-backed insights. Using cutting-edge Machine Learning, it predicts housing prices based on location, 
area, room count, and neighborhood sustainability — enabling smarter, eco-conscious urban decisions.
""")

st.divider()

# -----------------------------------------------------------
# TEAM SECTION
# -----------------------------------------------------------
st.markdown("<h2 class='section-title'>👥 Meet Our Team</h2>", unsafe_allow_html=True)
cols = st.columns(4)
for i, col in enumerate(cols, start=1):
    with col:
        st.markdown(f"""
        <div class="card">
            <h3>Teammate {i}</h3>
            <p>Role {i}</p>
            <p>🌐 <a href="#" style="color:#E2725B;text-decoration:none;">LinkedIn</a> | 💻 <a href="#" style="color:#E2725B;text-decoration:none;">GitHub</a></p>
        </div>
        """, unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------
# CONTACT FORM
# -----------------------------------------------------------
st.markdown("<h2 class='section-title'>📬 Contact Us</h2>", unsafe_allow_html=True)
st.markdown('<div class="contact-container">', unsafe_allow_html=True)
with st.form("contact_form"):
    name = st.text_input("Your Name", placeholder="Enter your full name")
    email = st.text_input("Your Email", placeholder="Enter your email address")
    message = st.text_area("Your Message", placeholder="Type your message here...")
    submitted = st.form_submit_button("Send Message")
    if submitted:
        st.markdown('<div class="contact-success">✅ Thank you for reaching out! Our team will get back to you soon.</div>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)

st.divider()

# -----------------------------------------------------------
# FUTURE SCOPE
# -----------------------------------------------------------
st.markdown("<h2 class='section-title'>🚀 Future Scope</h2>", unsafe_allow_html=True)
st.markdown("""
- 🌍 **Real-Time API Integration:** Integrate with live real estate APIs for dynamic, market-driven predictions and trend analysis.  
- ☁️ **Cloud Deployment:** Deploy StreetBase on scalable cloud platforms (AWS / GCP) for seamless performance and availability.  
- 🧠 **Explainable AI:** Implement SHAP and LIME for transparent, interpretable machine learning decisions.  
- 📊 **Advanced Visualization:** Add an interactive analytics dashboard showcasing sustainability metrics, growth potential, and location insights.  
""")

st.divider()

# -----------------------------------------------------------
# CONNECT WITH US
# -----------------------------------------------------------
st.markdown("<h2 class='section-title'>🌐 Connect With Us</h2>", unsafe_allow_html=True)
st.write("📧 streetbase@gmail.com")
st.write("🌍 www.streetbase.ai")

# QR Code Generation
qr = qrcode.make("https://github.com/your-project-repo")  # Replace with your GitHub repo link
buf = io.BytesIO()
qr.save(buf, format="PNG")
st.image(buf.getvalue(), width=130)

# -----------------------------------------------------------
# FOOTER
# -----------------------------------------------------------
st.markdown("""
<div class="footer">
    <b>StreetBase</b> © 2025 — Innovating Real Estate Intelligence with AI
</div>
""", unsafe_allow_html=True)


def load_about_us_page():
    import streamlit as st
    from components.NavBar.navbar import navbar

    navbar()

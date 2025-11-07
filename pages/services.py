import streamlit as st
from streamlit_lottie import st_lottie
import requests

# --- PAGE CONFIG ---
st.set_page_config(page_title="Our Services | AI Real Estate", page_icon="🏠", layout="wide")

# --- LOAD LOTTIE ANIMATION FUNCTION ---
# --- LOAD LOCAL LOTTIE JSON FILE ---
import json

def load_lottie_file(filepath: str):
    with open(filepath, "r") as f:
        return json.load(f)


# --- LOAD ANIMATIONS (AI, Analytics, Market Trend) ---
ai_data = load_lottie_file("../Assets/ai_data.json")
analytics_viz = load_lottie_file("../Assets/analytics_viz.json")
market_forecast = load_lottie_file("../Assets/market_forecast.json")

# --- CUSTOM CSS (animations + styling) ---
# --- CUSTOM CSS (Brand Palette: Light + Dark Ready) ---
st.markdown("""
    <style>
    body {
        font-family: 'Inter', sans-serif;
        background-color: #F2F2F6;
    }

    h2, h3, h4 {
        text-align: center;
        color: #003366;
    }
    h2 {
        font-weight: 800;
        margin-bottom: 0.4em;
    }
    h3 {
        color: #336699;
        margin-bottom: 2em;
    }

    /* Service Card Styling */
    .service-card {
        background-color: #FFFFFF;
        border-radius: 16px;
        box-shadow: 0 4px 20px rgba(0,0,0,0.05);
        padding: 30px;
        transition: all 0.4s ease;
        overflow: hidden;
        position: relative;
        border: 1px solid #CCCCCC;
    }
    .service-card:hover {
        transform: translateY(-6px) scale(1.02);
        box-shadow: 0 8px 25px rgba(0,51,102,0.2);
    }

    .lottie-container {
        transition: transform 0.4s ease;
    }
    .lottie-container:hover {
        transform: scale(1.1);
    }

    .benefits {
        text-align: left;
        font-size: 15px;
        color: #003366;
    }
    .benefits li {
        margin-bottom: 6px;
    }

    /* CTA Button Styling */
    .cta-button {
        background-color: #FF6600;
        color: white;
        border: none;
        border-radius: 8px;
        padding: 8px 16px;
        font-weight: 600;
        text-decoration: none;
        transition: 0.3s ease;
    }
    .cta-button:hover {
        background-color: #e65c00;
        transform: scale(1.05);
    }

    /* Pricing Table Styling */
    .pricing-table {
        width: 100%;
        border-collapse: collapse;
        margin-top: 40px;
        font-size: 15px;
        border: 1px solid #CCCCCC;
    }
    .pricing-table th, .pricing-table td {
        border: 1px solid #CCCCCC;
        padding: 14px;
        text-align: center;
    }
    .pricing-table th {
        background-color: #003366;
        color: white;
        font-weight: 700;
    }
    .pricing-table tr:nth-child(even) { background-color: #F2F2F6; }
    .pricing-table tr:hover { background-color: #E6E6E6; }

    /* Streamlit Page Background Override */
    [data-testid="stAppViewContainer"] {
        background-color: #F2F2F6;
    }

    /* Quote Form Styling */
    input, textarea, select {
        border-radius: 6px !important;
        border: 1px solid #CCCCCC !important;
        padding: 6px 10px !important;
    }

    </style>
""", unsafe_allow_html=True)


# --- PAGE HEADER ---
st.markdown("<h2>Our Services</h2>", unsafe_allow_html=True)
st.markdown("<h3>Empowering Real Estate Decisions with Artificial Intelligence</h3>", unsafe_allow_html=True)
st.write("")

# --- SERVICE DATA ---
services = [
    {
        "title": "AI & Data Prediction Services",
        "desc": "Get precise property valuations using AI models trained on historical market data and regional trends.",
        "benefits": [
            "Accurate and instant price estimates",
            "Data-driven decision making",
            "Localized model predictions",
            "Automated valuation insights"
        ],
        "animation": ai_data
    },
    {
        "title": "Analytics & Visualization Services",
        "desc": "Visualize property market trends through AI-powered dashboards and interactive analytics.",
        "benefits": [
            "Interactive charts & trend maps",
            "Real-time analytics dashboards",
            "Location-based market visualization",
            "Customizable reporting tools"
        ],
        "animation": analytics_viz
    },
    {
        "title": "Market Trend Forecasting",
        "desc": "Leverage machine learning to forecast future property price movements and demand fluctuations.",
        "benefits": [
            "AI-driven trend forecasting",
            "Region-wise growth prediction",
            "Investment timing recommendations",
            "Dynamic data visualization"
        ],
        "animation": market_forecast
    },
]

# --- DISPLAY SERVICE CARDS ---
for service in services:
    col1, col2 = st.columns([1.2, 1])
    with col1:
        st.markdown(f"""
        <div class="service-card">
            <h4>{service['title']}</h4>
            <p style='color:#555; font-size:16px;'>{service['desc']}</p>
            <ul class="benefits">
                {''.join(f"<li> {b}</li>" for b in service['benefits'])}
            </ul>
            <br>
            <a class="cta-button" href="#quote-form">Get Quote</a>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        with st.container():
            st.markdown("<div class='lottie-container'>", unsafe_allow_html=True)
            if service["animation"]:
                st_lottie(service["animation"], height=260, key=service["title"])
            else:
                st.info("Animation could not load.")
            st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("---")

# --- PRICING SECTION ---
st.markdown("<br><br><h2>Pricing Plans</h2>", unsafe_allow_html=True)
st.markdown("<h3>Choose the plan that fits your needs</h3>", unsafe_allow_html=True)
st.markdown("""
<table class="pricing-table">
    <tr>
        <th>Plan</th>
        <th>Features</th>
        <th>Ideal For</th>
        <th>Price</th>
    </tr>
    <tr>
        <td><b>Starter</b></td>
        <td>Basic predictions & analytics dashboard access</td>
        <td>Freelancers & students</td>
        <td><b>$49 / month</b></td>
    </tr>
    <tr>
        <td><b>Professional</b></td>
        <td>Advanced forecasts, API access, custom dashboards</td>
        <td>Startups & agencies</td>
        <td><b>$99 / month</b></td>
    </tr>
    <tr>
        <td><b>Enterprise</b></td>
        <td>Unlimited data, tailored AI models, team analytics</td>
        <td>Large enterprises</td>
        <td><b>$149/ month</b></td>
    </tr>
</table>
""", unsafe_allow_html=True)

# --- QUOTE FORM ---
st.markdown("<br><br><h2 id='quote-form'>Request a Quote</h2>", unsafe_allow_html=True)
st.markdown("<h3>Let’s build your AI-powered real estate solution</h3>", unsafe_allow_html=True)

with st.form("quote_form"):
    name = st.text_input("Full Name")
    email = st.text_input("Email Address")
    service_choice = st.selectbox("Service Interested In", [s["title"] for s in services])
    message = st.text_area("Additional Information or Requirements")
    submitted = st.form_submit_button("Submit Request")

    if submitted:
        if name and email:
            st.success(f"Thank you, {name}! Our team will reach out soon about {service_choice}.")
        else:
            st.warning("Please fill out your name and email before submitting.")

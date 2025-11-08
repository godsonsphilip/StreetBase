# --- put these 5 lines at the very top ---
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]  # points to .../SmartBricks
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
# -----------------------------------------

from components.NavBar.navbar import navbar

import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Case Studies | StreetBase AI", page_icon="🏙️", layout="wide")

st.markdown("""
    <style>
        /* Force light mode and readable text */
        html, body, [data-testid="stAppViewContainer"] {
            background: #ffffff !important;
            color: #1f2937 !important;
            font-family: 'Poppins', sans-serif;
        }
        h1, h2, h3, h4, h5, h6,
        p, span, li, strong, em, small,
        .stMarkdown, .stText, .stCaption, .stHeader,
        [data-testid="stMarkdownContainer"] {
            color: #1f2937 !important;
        }

        /* Titles */
        .title { 
            text-align:center; 
            font-size:2.6rem; 
            font-weight:700; 
            color:#002244 !important; 
            margin-top:.3em; 
            letter-spacing:.5px; 
        }
        .subtitle { 
            text-align:center; 
            font-size:1.15rem; 
            color:#4b5563 !important; 
            margin-bottom:2.2em; 
        }

        /* Card Design */
        .card { 
            background:#fff; 
            border-radius:18px; 
            box-shadow:0 3px 12px rgba(0,0,0,.08); 
            padding:1.2em; 
            transition:.3s; 
            height:100%; 
            cursor:pointer; 
            border-top:4px solid #FF6600; 
        }
        .card:hover { 
            transform:translateY(-6px); 
            box-shadow:0 6px 18px rgba(0,0,0,.15); 
        }
        .card img { 
            border-radius:12px; 
            margin-bottom:1em; 
            width:100%; 
            height:180px; 
            object-fit:cover; 
        }
        .card-title { 
            color:#003366 !important; 
            font-size:1.25rem; 
            font-weight:700; 
            margin-bottom:.3em; 
        }
        .card-location { 
            color:#FF6600 !important; 
            font-weight:600; 
            font-size:.9rem; 
            margin-bottom:.5em; 
        }
        .card-text { 
            color:#374151 !important; 
            font-size:.95rem; 
            line-height:1.55; 
        }

        /* Detail box */
        .detail-box { 
            background:#fff; 
            border-radius:16px; 
            box-shadow:0 4px 14px rgba(0,0,0,.08); 
            padding:2em; 
            margin-top:1.5em; 
        }
        .detail-box * { color:#1f2937 !important; }
        .detail-title { 
            font-size:1.4rem; 
            font-weight:700; 
            margin:0 0 .6rem 0; 
        }
        .detail-img { 
            width:100%; 
            height:260px; 
            object-fit:cover; 
            border-radius:12px; 
            margin:.6rem 0 1rem 0; 
        }
        .metric { 
            background:#f5f8ff; 
            border-left:5px solid #4B8BFF; 
            padding:12px 16px; 
            border-radius:10px; 
            font-size:.95rem; 
            margin:6px 0; 
        }
        .impact { 
            background:#FFF5E6; 
            border-left:5px solid #FF6600; 
            padding:12px 16px; 
            border-radius:10px; 
            font-size:.95rem; 
            margin:6px 0; 
        }

        /* ✅ Button Styling — White by default, light orange on hover */
        .stButton > button {
            background-color: #ffffff !important;
            color: #002244 !important;
            border: 1.5px solid #FF6600 !important;
            border-radius: 10px !important;
            padding: 0.6em 1.2em !important;
            font-weight: 600 !important;
            transition: all 0.25s ease-in-out;
        }
        .stButton > button:hover {
            background-color: #FFD8B0 !important; /* Light orange hover */
            color: #002244 !important;
            border-color: #FF6600 !important;
        }
        .stButton > button:focus {
            outline: 2px solid #FFB366 !important;
            outline-offset: 2px !important;
        }

        /* Captions & Links */
        a { color:#002244 !important; text-decoration:none !important; }
        .caption, .stCaption { color:#6b7280 !important; }

        /* Footer */
        footer { display:none; }
    </style>
""", unsafe_allow_html=True)





navbar()  # your custom navbar (includes Login/Signup buttons)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>🏗️ Case Studies</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Real-world AI Transformations in India's Real Estate Market</div>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# ---------------- CASE STUDY GRID ----------------
if not st.session_state.selected_case:
    st.markdown("""
    <div style='text-align: center; font-size: 1.3rem; font-weight: 500; color: #333; margin-bottom: 1.5em;'> 🌍 Explore how AI is reshaping the Indian property landscape </div>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🏢 Mumbai — AI-Driven Apartment Valuation"):
            st.session_state.selected_case = "mumbai"
            st.rerun()
        st.image("https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=800&q=80")
        st.caption("AI models bring price accuracy and speed to Mumbai’s complex housing market.")

    with col2:
        if st.button("📊 Bengaluru — Predictive Market Insights"):
            st.session_state.selected_case = "bengaluru"
            st.rerun()
        st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80")
        st.caption("Forecasting property trends and demand with deep learning time-series models.")

    with col3:
        if st.button("🏙️ Delhi NCR — Smart Property Comparison"):
            st.session_state.selected_case = "delhi"
            st.rerun()
        st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=80")
        st.caption("AI-powered ranking engine for better investment decisions and faster deals.")

else:
    # ---------------- DETAILED VIEWS (rendered as one HTML block so content stays inside the box) ----------------
    case = st.session_state.selected_case

    if case == "mumbai":
        title = "🏢 AI-Driven Apartment Valuation — Mumbai, India"
        overview = """Mumbai's real estate market is fast, fragmented, and highly price-sensitive.
        SmartBricks’ <b>AI-powered valuation system</b> automated what used to take <b>weeks</b> into seconds — ensuring fair, data-backed pricing."""
        image = "https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=1200&q=80"
        metrics = [
            "📊 10,000+ apartments analyzed using Random Forest & XGBoost",
            "⚙️ Achieved R² = 0.94 | MAE = ₹3.1 lakhs",
        ]
        impacts = [
            "💡 Reduced manual appraisal time by 90%",
            "🏦 Adopted by 5 major property lenders for loan risk assessment",
            "📈 Helped standardize price variance across suburbs",
        ]

    elif case == "bengaluru":
        title = "📊 Predictive Market Insights — Bengaluru, India"
        overview = """Bengaluru’s housing demand mirrors its booming tech industry.
        Using <b>LSTM-based time series models</b>, StreetBase delivers live forecasts of housing prices and investment growth corridors."""
        image = "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=1200&q=80"
        metrics = [
            "🧠 LSTM + Prophet ensemble model for 7 years of transaction data",
            "🔍 Incorporated IT job data, metro expansions, and infra growth",
        ]
        impacts = [
            "🚀 93% forecast accuracy — helping developers plan smarter",
            "💬 Realtors close deals 25% faster using AI-driven dashboards",
        ]

    else:  # delhi
        title = "🏙️ Smart Property Comparison Tool — Delhi NCR, India"
        overview = """Delhi NCR buyers face overwhelming property choices.
        SmartBricks’ <b>AI recommendation engine</b> ranks properties based on ROI, amenities, and proximity — saving users hours of research."""
        image = "https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=1200&q=80"
        metrics = [
            "⚖️ Ranking model powered by cosine similarity and weighted ROI",
            "📉 Reduced search and decision time by 60%",
        ]
        impacts = [
            "🏘️ Integrated by 4+ real estate startups",
            "🧩 Increased client conversion by 35% through better matching",
        ]

    # Build the whole detail box as one HTML string so everything stays inside
    metrics_html = "".join([f"<div class='metric'>{m}</div>" for m in metrics])
    impacts_html = "".join([f"<div class='impact'>{i}</div>" for i in impacts])

    detail_html = f"""
    <div class='detail-box'>
        <div class='detail-title'>{title}</div>
        <img src="{image}" class="detail-img" />
        <p>{overview}</p>
        {metrics_html}
        {impacts_html}
    </div>
    """

    st.markdown(detail_html, unsafe_allow_html=True)

    # Back button (styled by global .stButton CSS)
    if st.button("⬅️ Back to All Case Studies"):
        st.session_state.selected_case = None
        st.rerun()


# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#666;'>© 2025 StreetBase | Empowering Indian Real Estate with AI-Driven Insights</p>",
    unsafe_allow_html=True
)

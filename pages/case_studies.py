import streamlit as st
from components.NavBar.navbar import navbar

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Case Studies | StreetBase AI", page_icon="🏙️", layout="wide")

# ---------------- CUSTOM STYLES ----------------
st.markdown("""
    <style>
        /* General Styling */
        body { background-color: #f9fafc; font-family: 'Poppins', sans-serif; }

        /* Titles */
        .title {
            text-align: center;
            font-size: 2.6rem;
            font-weight: 700;
            color: #002244;
            margin-top: 0.3em;
            letter-spacing: 0.5px;
        }
        .subtitle {
            text-align: center;
            font-size: 1.15rem;
            color: #666;
            margin-bottom: 2.2em;
        }

        /* Case Study Cards */
        .card {
            background-color: white;
            border-radius: 18px;
            box-shadow: 0 3px 12px rgba(0,0,0,0.08);
            padding: 1.2em;
            transition: 0.3s;
            height: 100%;
            cursor: pointer;
            border-top: 4px solid #FF6600;
        }
        .card:hover {
            transform: translateY(-6px);
            box-shadow: 0 6px 18px rgba(0,0,0,0.15);
        }
        .card img {
            border-radius: 12px;
            margin-bottom: 1em;
            width: 100%;
            height: 180px;
            object-fit: cover;
        }
        .card-title {
            color: #003366;
            font-size: 1.25rem;
            font-weight: 700;
            margin-bottom: 0.3em;
        }
        .card-location {
            color: #FF6600;
            font-weight: 600;
            font-size: 0.9rem;
            margin-bottom: 0.5em;
        }
        .card-text {
            color: #333;
            font-size: 0.9rem;
            line-height: 1.5;
        }

        /* Detail section */
        .detail-box {
            background-color: #ffffff;
            border-radius: 16px;
            box-shadow: 0 4px 14px rgba(0,0,0,0.08);
            padding: 2em;
            margin-top: 1.5em;
        }
        .metric {
            background-color: #f5f8ff;
            border-left: 5px solid #4B8BFF;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 0.95rem;
            margin: 6px 0;
        }
        .impact {
            background-color: #FFF5E6;
            border-left: 5px solid #FF6600;
            padding: 12px 16px;
            border-radius: 10px;
            font-size: 0.95rem;
            margin: 6px 0;
        }
        .btn-back {
            text-align: center;
            margin-top: 1.2em;
        }
        .btn-back button {
            background-color: #003366 !important;
            color: white !important;
            border-radius: 10px;
            padding: 0.6em 1.5em;
            font-weight: 600;
        }
        .btn-back button:hover {
            background-color: #004B8D !important;
        }
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
    # ---------------- DETAILED VIEWS ----------------
    st.markdown("<div class='detail-box'>", unsafe_allow_html=True)

    if st.session_state.selected_case == "mumbai":
        st.subheader("🏢 AI-Driven Apartment Valuation — Mumbai, India")
        st.write("""
        Mumbai's real estate market is fast, fragmented, and highly price-sensitive.  
        SmartBricks’ **AI-powered valuation system** automated what used to take **weeks** into seconds — ensuring fair, data-backed pricing.
        """)
        st.markdown("<div class='metric'>📊 10,000+ apartments analyzed using Random Forest & XGBoost</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric'>⚙️ Achieved R² = 0.94 | MAE = ₹3.1 lakhs</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>💡 Reduced manual appraisal time by 90%</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>🏦 Adopted by 5 major property lenders for loan risk assessment</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>📈 Helped standardize price variance across suburbs</div>", unsafe_allow_html=True)

    elif st.session_state.selected_case == "bengaluru":
        st.subheader("📊 Predictive Market Insights — Bengaluru, India")
        st.write("""
        Bengaluru’s housing demand mirrors its booming tech industry.  
        Using **LSTM-based time series models**, StreetBase delivers live forecasts of housing prices and investment growth corridors.
        """)
        st.markdown("<div class='metric'>🧠 LSTM + Prophet ensemble model for 7 years of transaction data</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric'>🔍 Incorporated IT job data, metro expansions, and infra growth</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>🚀 93% forecast accuracy — helping developers plan smarter</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>💬 Realtors close deals 25% faster using AI-driven dashboards</div>", unsafe_allow_html=True)

    elif st.session_state.selected_case == "delhi":
        st.subheader("🏙️ Smart Property Comparison Tool — Delhi NCR, India")
        st.write("""
        Delhi NCR buyers face overwhelming property choices.  
        SmartBricks’ **AI recommendation engine** ranks properties based on ROI, amenities, and proximity — saving users hours of research.
        """)
        st.markdown("<div class='metric'>⚖️ Ranking model powered by cosine similarity and weighted ROI</div>", unsafe_allow_html=True)
        st.markdown("<div class='metric'>📉 Reduced search and decision time by 60%</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>🏘️ Integrated by 4+ real estate startups</div>", unsafe_allow_html=True)
        st.markdown("<div class='impact'>🧩 Increased client conversion by 35% through better matching</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.markdown("<div class='btn-back'>", unsafe_allow_html=True)
    if st.button("⬅️ Back to All Case Studies"):
        st.session_state.selected_case = None
        st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#666;'>© 2025 StreetBase | Empowering Indian Real Estate with AI-Driven Insights</p>",
    unsafe_allow_html=True
)
def load_case_studies_page():
    import streamlit as st
    from components.NavBar.navbar import navbar
    
    navbar()
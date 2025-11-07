import streamlit as st

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Case Studies | AI Real Estate", page_icon="🏙️", layout="wide")

# ---------------- STYLES ----------------
st.markdown("""
    <style>
        .title {
            text-align: center;
            font-size: 2.3rem;
            font-weight: 700;
            color: #003366;
            margin-top: 0.5em;
        }
        .subtitle {
            text-align: center;
            font-size: 1.1rem;
            color: #666;
            margin-bottom: 2em;
        }
        .card {
            background-color: white;
            border-radius: 16px;
            box-shadow: 0 3px 10px rgba(0,0,0,0.08);
            padding: 1em;
            transition: 0.3s;
            height: 100%;
            cursor: pointer;
        }
        .card:hover {
            transform: scale(1.03);
            box-shadow: 0 6px 16px rgba(0,0,0,0.15);
        }
        .card img {
            border-radius: 12px;
            margin-bottom: 1em;
            width: 100%;
            height: 160px;
            object-fit: cover;
        }
        .card-title {
            color: #003366;
            font-size: 1.2rem;
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
    </style>
""", unsafe_allow_html=True)

# ---------------- HEADER ----------------
st.markdown("<div class='title'>Case Studies</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>AI-Based Real Estate Valuation System — Indian Era</div>", unsafe_allow_html=True)

# ---------------- SESSION STATE ----------------
if "selected_case" not in st.session_state:
    st.session_state.selected_case = None

# ---------------- CASE STUDIES GRID ----------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🏢 AI-Driven Apartment Valuation (Mumbai)"):
        st.session_state.selected_case = "mumbai"
        st.rerun()
    st.image("https://images.unsplash.com/photo-1582407947304-fd86f028f716?auto=format&fit=crop&w=800&q=80")
    st.caption("AI instantly values Mumbai apartments with 95% accuracy — replacing 2-week manual appraisals.")

with col2:
    if st.button("📊 Predictive Market Insights (Bengaluru)"):
        st.session_state.selected_case = "bengaluru"
        st.rerun()
    st.image("https://images.unsplash.com/photo-1504384308090-c894fdcc538d?auto=format&fit=crop&w=800&q=80")
    st.caption("AI predicts live Bengaluru real estate price trends, improving forecasting and investment planning.")

with col3:
    if st.button("🏙️ Smart Property Comparison (Delhi NCR)"):
        st.session_state.selected_case = "delhi"
        st.rerun()
    st.image("https://images.unsplash.com/photo-1568605114967-8130f3a36994?auto=format&fit=crop&w=800&q=80")
    st.caption("AI system ranks Delhi properties by ROI — saving 60% of buyers’ research time.")

st.markdown("---")

# ---------------- DETAILED SECTIONS ----------------
if st.session_state.selected_case == "mumbai":
    st.subheader("🏢 AI-Driven Apartment Valuation — Mumbai, India")
    st.write("""
    In Mumbai’s fast-paced real estate market, manual appraisals took weeks and often varied across agents.
    The AI valuation model now predicts property prices in **seconds**, maintaining consistent accuracy.

    **Highlights:**
    - 10,000+ apartment records from multiple Mumbai suburbs  
    - Trained using Random Forest & XGBoost  
    - Achieved **R² = 0.94**, MAE = ₹3.1 lakhs  
    - Reduced human appraisal time by **90%**  

    **Impact:**  
    Property developers and financial institutions now rely on this system for instant valuations and loan approvals.
    """)

elif st.session_state.selected_case == "bengaluru":
    st.subheader("📊 Predictive Market Insights — Bengaluru, India")
    st.write("""
    Bengaluru’s IT corridor drives constant housing demand. 
    AI models here analyze **past 7 years of transaction data** and predict price changes using **LSTM networks**.

    **Approach:**
    - Time-series forecasting of market price per sqft  
    - Integrated metro expansion and IT job growth data  
    - Deployed live dashboard with Streamlit for insights  

    **Results:**
    - **93% prediction accuracy**  
    - Realtors now close deals **25% faster** with confidence in AI-backed insights.  
    """)

elif st.session_state.selected_case == "delhi":
    st.subheader("🏙️ Smart Property Comparison Tool — Delhi NCR, India")
    st.write("""
    In Delhi NCR, homebuyers struggled with too many options.  
    Our system uses AI ranking and **cosine similarity** to match users with the best-fit property.

    **Features:**
    - Ranking based on area, price, and location proximity  
    - Visualization chart for ROI vs amenities  
    - Integrated recommendation model  

    **Results:**
    - **60% time saved** in property comparison  
    - Used by 4+ local real estate startups for client assistance.  
    """)

else:
    st.info("👆 Click on any case study above to view detailed AI-driven insights from the Indian real estate market.")

# ---------------- FOOTER ----------------
st.markdown("---")
st.markdown(
    "<p style='text-align:center; color:#555;'>🏗️ AI Transforming Indian Real Estate | Case Studies Dashboard</p>",
    unsafe_allow_html=True
)

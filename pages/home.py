# pages/home.py
import os
import sys
import streamlit as st
from pathlib import Path
import joblib
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import io
import time

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
# from components.simple_app import load_valuation_section  # ✅ NEW IMPORT

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="StreetBase | Home",
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
        /* Ensure Streamlit widget labels are visible */
        label, .stNumberInput label, .stSelectbox label, .stMultiSelect label, .stTextInput label {
            color: #003366 !important;
            font-weight: 700 !important;
            font-size: 14px !important;
            display: block !important;
            margin-bottom: 6px !important;
        }
        /* Ensure tab labels are visible and not clipped */
        .stTabs [data-baseweb="tab"] {
            color: #003366 !important;
            background-color: transparent !important;
            font-weight: 700 !important;
            -webkit-text-fill-color: initial !important;
            -webkit-background-clip: initial !important;
        }
        .stTabs [aria-selected="true"] {
            color: #FFFFFF !important;
            background: linear-gradient(135deg, #003366 0%, #004080 100%) !important;
            box-shadow: 0 6px 20px rgba(0,51,102,0.25) !important;
            border-color: #003366 !important;
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


# ---------------- VALUATION SECTION ----------------
st.markdown("<section>", unsafe_allow_html=True)
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("<h2 style='text-align:center; color:#003366;'>💰 Property Valuation</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; color:#444;'>Try our AI-powered valuation engine below</p>", unsafe_allow_html=True)

# --- Inlined premium enhanced valuation UI (adapted) ---


def load_valuation_section():
    # Inject premium CSS/theme (scoped)
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
        * { font-family: 'Inter', 'Segoe UI', sans-serif; }
        .stApp { background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%); }
        .main-header { text-align:center; padding:30px 0; background:linear-gradient(135deg,#FFFFFF 0%, #F8F9FA 100%); border-radius:20px; box-shadow:0 8px 32px rgba(0,0,0,0.1); margin-bottom:40px; }
        .gradient-text { font-size:2.4em; font-weight:800; background: linear-gradient(135deg, #003366 0%, #FF6600 100%); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text; margin:0; }
        .sub-header { color:#666; font-size:1.1em; margin-top:8px; font-weight:500; }
        .section-header { background: linear-gradient(135deg, #003366 0%, #004080 100%); padding:20px; border-radius:14px; margin-bottom:20px; }
        .section-title { color:white; margin:0; font-size:1.5em; font-weight:700; }
        .section-subtitle { color:#E6F0FF; margin-top:8px; font-size:0.95em; }
        .preset-card { padding:18px; border-radius:12px; text-align:center; margin-bottom:12px; box-shadow:0 6px 20px rgba(0,0,0,0.08); }
        .preset-icon { font-size:28px; margin-bottom:6px; }
        .preset-title { font-size:16px; font-weight:700; color:#003366; }
        .stButton>button { background: linear-gradient(90deg,#ff7a00,#ff9f3a) !important; color:#fff !important; border-radius:8px !important; height:44px !important; font-weight:700 !important; }
        .property-card { border:2px solid #ff7a00; border-radius:14px; padding:16px; background: linear-gradient(90deg,#fffaf7,#fff6f0); box-shadow:0 12px 40px rgba(0,0,0,0.06); margin-top:12px; }
        .stNumberInput input, .stSelectbox select, .stTextInput input { border-radius:8px; padding:10px; }
        hr { border:none; height:4px; background: linear-gradient(90deg, transparent 0%, #FF6600 50%, transparent 100%); margin:24px 0; }
    </style>
    """, unsafe_allow_html=True)

    # Header
    st.markdown("""
        <div class='main-header'>
            <h1 class='gradient-text'>🏠 Real Estate Price Prediction</h1>
            <p class='sub-header'>Powered by AI • Instant Estimates • Market Insights</p>
        </div>
    """, unsafe_allow_html=True)

    # Helpers and assets
    ROOT_ASSETS = Path(ROOT) / 'Assets'
    MODEL_FILE = ROOT_ASSETS / 'real_estate_model.pkl'
    DATA_FILE = ROOT_ASSETS / 'india_housing_prices.csv'

    def load_model_metadata(path=MODEL_FILE):
        if path.exists():
            try:
                meta = joblib.load(path)
                if isinstance(meta, dict) and 'model' in meta:
                    return meta
                else:
                    return {'model': meta, 'feature_names': None, 'target_name': None}
            except Exception as e:
                st.warning(f"Failed to load model metadata: {e}")
                return None
        return None

    def fmt_currency(x):
        try:
            return f"₹{float(x):,.2f}"
        except Exception:
            return str(x)

    def df_median_or_default(df, col, default=0):
        try:
            if df is not None and col in df.columns:
                return float(df[col].median())
        except Exception:
            pass
        return default

    # Load model
    # Debug: Show the path being checked
    if not MODEL_FILE.exists():
        st.error(f"❌ Model not found at: {MODEL_FILE}")
        st.info(f"📁 Current working directory: {Path.cwd()}")
        st.info(f"📂 ROOT directory: {ROOT}")
        st.info(f"📂 ROOT_ASSETS directory: {ROOT_ASSETS}")
        return
    
    meta = load_model_metadata()
    if not meta:
        st.error("❌ Failed to load model. Please check the model file format.")
        return

    model = meta.get('model')
    feature_names = meta.get('feature_names', []) or []
    if not model or not feature_names:
        st.error("❌ Invalid model metadata")
        return

    # Load dataset for defaults
    df = None
    if DATA_FILE.exists():
        try:
            df = pd.read_csv(DATA_FILE)
        except Exception:
            df = None

    # Session state
    if 'prediction_history' not in st.session_state:
        st.session_state.prediction_history = []
    # NOTE: presets removed — no preset session state maintained

    # Tabs
    tab1, tab2, tab3 = st.tabs(["🔮 Predict", "📊 History", "📈 Market Insights"])

    with tab1:
        st.markdown("""
            <div class='section-header'>
                <h2 class='section-title'>🔮 Property Price Estimator</h2>
                <p class='section-subtitle'>Get instant AI-powered price estimates for properties across India</p>
            </div>
        """, unsafe_allow_html=True)

        # Quick presets removed per user request

        # Prediction form
        with st.form("prediction_form"):
            st.markdown("<h3 style='color: #003366; margin-bottom: 18px;'>📝 Property Details</h3>", unsafe_allow_html=True)

            # Presets removed — use empty defaults (or dataset medians)
            preset_vals = {}

            c1, c2 = st.columns(2)
            with c1:
                if df is not None and 'State' in df.columns:
                    state_options = sorted(df['State'].unique().tolist())
                else:
                    state_options = ['Andhra Pradesh', 'Assam', 'Bihar', 'Delhi', 'Gujarat', 'Karnataka', 'Maharashtra', 'Tamil Nadu']
                state = st.selectbox("🗺️ State", options=state_options, key="state_input")

                if df is not None and 'State' in df.columns and 'City' in df.columns:
                    filtered_cities = df[df['State'] == state]['City'].unique().tolist()
                    city_options = sorted(filtered_cities) if filtered_cities else ['No cities available']
                else:
                    city_options = ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Hyderabad']
                city = st.selectbox("🏙️ City", options=city_options, key="city_input")

                area = st.number_input("📐 Area (sqft)", min_value=100, max_value=50000, value=preset_vals.get('Area', int(df_median_or_default(df, 'Area', 1000))), step=100)
                bhk = st.number_input("🏘️ BHK", min_value=1, max_value=10, value=preset_vals.get('BHK', int(df_median_or_default(df, 'BHK', 2))), step=1)

            with c2:
                bedrooms = st.number_input("🛏️ Bedrooms", min_value=1, max_value=20, value=preset_vals.get('Bedroom', int(df_median_or_default(df, 'Bedroom', 2))), step=1)
                bathrooms = st.number_input("🚿 Bathrooms", min_value=1, max_value=10, value=preset_vals.get('Bathroom', int(df_median_or_default(df, 'Bathroom', 2))), step=1)
                balconies = st.number_input("🌅 Balconies", min_value=0, max_value=10, value=int(df_median_or_default(df, 'Balcony', 1)), step=1)

            st.markdown("<h4 style='color: #003366; margin: 20px 0 12px 0;'>✨ Amenities</h4>", unsafe_allow_html=True)
            amenity_options = ['Parking', 'Gym', 'Swimming Pool', 'Garden', 'Security', 'Power Backup', 'Hospitals', 'Schools']
            selected_amenities = st.multiselect("Select amenities", options=amenity_options, default=[])

            st.markdown("<br>", unsafe_allow_html=True)
            prediction_button = st.form_submit_button("🔍 Get Price Estimate", use_container_width=True)

            if prediction_button:
                with st.spinner("🔄 Analyzing property data with AI..."):
                    time.sleep(0.8)

                    input_data = {
                        'State': state,
                        'City': city,
                        'Area': area,
                        'BHK': bhk,
                        'Bedroom': bedrooms,
                        'Bathroom': bathrooms,
                        'Balcony': balconies,
                        'Parking': 1 if 'Parking' in selected_amenities else 0,
                        'Gym': 1 if 'Gym' in selected_amenities else 0,
                        'SwimmingPool': 1 if 'Swimming Pool' in selected_amenities else 0,
                        'Garden': 1 if 'Garden' in selected_amenities else 0,
                        'Security': 1 if 'Security' in selected_amenities else 0,
                        'PowerBackup': 1 if 'Power Backup' in selected_amenities else 0,
                        'Hospitals': 1 if 'Hospitals' in selected_amenities else 0,
                        'Schools': 1 if 'Schools' in selected_amenities else 0
                    }

                    for feat in feature_names:
                        if feat not in input_data:
                            input_data[feat] = 0

                    X_input = pd.DataFrame([input_data])[feature_names]
                    pred = model.predict(X_input)[0]

                    st.markdown(f"""
                        <div style='background: linear-gradient(135deg, #E6F7F0 0%, #D1F2E8 100%); padding: 30px; border-radius: 16px; border-left: 8px solid #00CC66; box-shadow: 0 8px 32px rgba(0,204,102,0.18); margin: 20px 0;'>
                            <div style='text-align:center;'>
                                <div style='font-size:1.1em; color:#00CC66; font-weight:700; margin-bottom:8px;'>✅ ESTIMATED PROPERTY VALUE</div>
                                <div style='font-size:2.8em; color:#003366; font-weight:800;'>{fmt_currency(pred)} <span style='font-size:0.55em;'>Lakhs</span></div>
                                <div style='color:#666; margin-top:8px;'>🤖 AI-Powered Prediction • ⚡ Instant Results • 📊 Data-Driven</div>
                            </div>
                        </div>
                    """, unsafe_allow_html=True)

                    history_entry = {
                        'Timestamp': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        'State': state,
                        'City': city,
                        'Area_sqft': area,
                        'BHK': bhk,
                        'Bedrooms': bedrooms,
                        'Bathrooms': bathrooms,
                        'Predicted_Price_Lakhs': f"{fmt_currency(pred)} Lakhs"
                    }
                    st.session_state.prediction_history.append(history_entry)

    with tab2:
        st.markdown("""
            <div class='section-header'>
                <h2 class='section-title'>📊 Prediction History</h2>
                <p class='section-subtitle'>Track all your property valuations in one place</p>
            </div>
        """, unsafe_allow_html=True)

        if st.session_state.prediction_history:
            df_history = pd.DataFrame(st.session_state.prediction_history)
            st.dataframe(df_history, use_container_width=True)

            col1, col2 = st.columns(2)
            with col1:
                csv = df_history.to_csv(index=False).encode('utf-8')
                st.download_button(label="📥 Download History (CSV)", data=csv, file_name=f"prediction_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", mime="text/csv", use_container_width=True)
            with col2:
                if st.button("🗑️ Clear History", use_container_width=True, key="clear_hist"):
                    st.session_state.prediction_history = []
                    st.rerun()
        else:
            st.info("📝 No predictions yet. Start by making a prediction in the Predict tab!")

    with tab3:
        st.markdown("""
            <div class='section-header'>
                <h2 class='section-title'>📈 Market Insights</h2>
                <p class='section-subtitle'>Explore comprehensive real estate market analytics and trends</p>
            </div>
        """, unsafe_allow_html=True)

        if df is not None:
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("📊 Total Properties", f"{len(df):,}", delta="Live Data")
            with c2:
                avg_price = df['Price_in_Lakhs'].mean() if 'Price_in_Lakhs' in df.columns else 0
                st.metric("💰 Avg Price", f"{fmt_currency(avg_price)} L", delta="+5.2%")
            with c3:
                cities = df['City'].nunique() if 'City' in df.columns else 0
                st.metric("🏙️ Cities Covered", f"{cities}", delta="Growing")

            st.markdown("<hr>", unsafe_allow_html=True)

            if 'Price_in_Lakhs' in df.columns:
                fig = px.histogram(df, x='Price_in_Lakhs', nbins=50, title='📊 Price Distribution', color_discrete_sequence=['#FF6600'])
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter, sans-serif', size=14), title_font=dict(size=20, color='#003366', family='Inter, sans-serif', weight='bold'))
                st.plotly_chart(fig, use_container_width=True)

            if 'City' in df.columns and 'Price_in_Lakhs' in df.columns:
                city_avg = df.groupby('City')['Price_in_Lakhs'].mean().sort_values(ascending=False).head(10)
                fig = px.bar(x=city_avg.index, y=city_avg.values, title='🏙️ Average Price by Top 10 Cities', labels={'x': 'City', 'y': 'Average Price (Lakhs)'}, color=city_avg.values, color_continuous_scale=[[0, '#003366'], [1, '#FF6600']])
                fig.update_layout(plot_bgcolor='white', paper_bgcolor='white', font=dict(family='Inter, sans-serif', size=14), title_font=dict(size=20, color='#003366', family='Inter, sans-serif', weight='bold'), showlegend=False)
                st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📊 No market data available. Load 'india_housing_prices.csv' for insights.")

    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🏠 <strong>AI Property Valuation Tool</strong> | Professional Real Estate Analysis</p>
    </div>
    """, unsafe_allow_html=True)

# Call the inlined enhanced UI
load_valuation_section()

st.markdown("</section>", unsafe_allow_html=True)

# ---------------- FOOTER ----------------
st.markdown("<br><br>", unsafe_allow_html=True)

# ---------------- FEATURES SECTION ----------------
load_feature_section()

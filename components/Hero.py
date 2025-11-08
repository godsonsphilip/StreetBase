import streamlit as st
from streamlit_lottie import st_lottie # Keeping Lottie in case we want to use it elsewhere, though not in this specific reference image
import requests # Also keeping for Lottie if needed
import os
# --- Page Configuration ---
st.set_page_config(
    page_title="StreetBase - AI Real Estate Valuation",
    page_icon="🏠",
    layout="wide" # Use wide layout for more space
    # initial_sidebar_state="expanded" # Optional: if you had a sidebar
)

# --- Custom CSS Injection (To match the reference image closely) ---
def custom_css_injection():
    """
    Injects custom CSS to style the Streamlit elements according to the reference image.
    """
    custom_css = """
    <style>
        /* --- Import Google Font 'Inter' (similar to reference) --- */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

        html, body, [data-testid="stAppViewContainer"] {
            font-family: 'Inter', sans-serif;
            color: #333333;
            background-color: #F8F9FA; /* Light grey background for the whole app */
        }
        
        /* Main container for the hero section to control its background and padding */
        .main-hero-container {
            background-color: #FFFFFF; /* White background for the main content area */
            border-radius: 12px;
            padding: 3rem; /* Generous padding */
            box-shadow: 0 4px 10px rgba(0,0,0,0.05); /* Subtle shadow */
            margin-bottom: 2rem;
            display: flex; /* Use flexbox for inner layout */
            align-items: center; /* Vertically align items */
        }
        
        /* Specific styling for the right insights column */
        .quick-insights-box {
            background-color: #EBF2FF; /* Light blue background for the insights box */
            border-radius: 12px;
            padding: 2rem;
            margin-left: 2rem; /* Space from left column */
            height: 100%; /* Ensure it fills height of its parent container */
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
        }
        
        /* --- Text Styling --- */
        h1 {
            font-size: 2.8rem !important; /* Larger, bolder title */
            font-weight: 800 !important;
            color: #002D62 !important; /* Dark blue */
            line-height: 1.1;
            margin-bottom: 0.5rem;
        }
        
        h2 { /* Quick Insights title */
            font-size: 1.6rem !important;
            font-weight: 700 !important;
            color: #0047AB !important; /* Medium blue */
            margin-bottom: 1.5rem !important;
        }

        /* Subheader like "Ready to Evaluate Your Property?" */
        .cta-banner h2 {
            font-size: 2.2rem !important;
            font-weight: 700 !important;
            color: #FFFFFF !important; /* White for the dark banner */
            text-align: center;
            margin-bottom: 1rem !important;
        }
        
        p, .stMarkdown, .stText {{
            font-size: 1.05rem;
            line-height: 1.6;
            color: #4A4A4A;
        }}
        
        /* Bullet points with emojis */
        ul li {{
            margin-bottom: 0.5rem;
            font-size: 1.05rem;
            color: #4A4A4A;
        }}
        .insights-list li { /* Specific styling for quick insights list */
            list-style: none; /* Remove default bullet */
            margin-bottom: 0.7rem;
            font-size: 1.05rem;
            color: #333333;
        }
        .insights-list li::before {
            content: "✅"; /* Checkmark emoji */
            margin-right: 0.8em;
        }

        /* --- Button Styling --- */
        .stButton > button {
            border-radius: 8px !important;
            font-weight: 600 !important;
            padding: 12px 25px !important; /* Good size */
            font-size: 1rem !important;
            transition: all 0.2s ease-in-out !important;
            border: none !important;
            box-shadow: 0 4px 8px rgba(0,0,0,0.1);
        }

        .stButton > button[kind="primary"] {
            background-color: #007BFF !important; /* Primary blue */
            color: white !important;
            margin-right: 15px; /* Space between buttons */
        }

        .stButton > button[kind="primary"]:hover {
            background-color: #0056b3 !important; /* Darker blue on hover */
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            transform: translateY(-2px);
        }

        .stButton > button[kind="secondary"] {
            background-color: #28A745 !important; /* Green for 'View Insights' */
            color: white !important;
        }
        
        .stButton > button[kind="secondary"]:hover {
            background-color: #218838 !important; /* Darker green on hover */
            box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
            transform: translateY(-2px);
        }

        /* --- Logo and Title at Top Left --- */
        .logo-container {
            display: flex;
            align-items: center;
            gap: 10px; /* Space between logo and text */
            margin-bottom: 2rem;
            padding: 1.5rem 0; /* Padding around the logo/brand */
        }
        .logo-img {
            height: 40px; /* Size of the house icon */
        }
        .brand-title {
            font-size: 1.8rem;
            font-weight: 700;
            color: #002D62;
            margin: 0; /* Remove default margins */
        }

        /* --- Bottom CTA Banner --- */
        .cta-banner {
            background-color: #007BFF; /* A solid blue for the banner */
            color: white;
            border-radius: 12px;
            padding: 3rem 2rem;
            text-align: center;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
            margin-top: 3rem; /* Space from the main content */
        }
        .cta-banner .emoji {
            font-size: 3rem; /* Size of the rocket emoji */
            margin-bottom: 1rem;
            display: block; /* Make it a block element to center */
        }
        .cta-banner p {
            color: #EBF2FF; /* Lighter white for body text */
            max-width: 800px;
            margin: 0 auto; /* Center the paragraph */
            font-size: 1.1rem;
        }
        
        /* Remove default Streamlit header/footer */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

    </style>
    """
    st.markdown(custom_css, unsafe_allow_html=True)

# --- Components for Member 2 ---

# Function for the logo and brand title
# Function for the logo and brand title using a local file
def render_brand_header():
    from pathlib import Path

    # Placeholder path — you can update this with your actual local logo path
    logo_path = os.path.join(os.path.dirname(__file__), "NavBar", "logo3.png") # <-- Replace with your actual file path

    st.markdown(
        """
        <div class="logo-container">
        """,
        unsafe_allow_html=True
    )

    # Display local logo
    st.image(str(logo_path), width=40)  # Width matches previous styling

    # Brand title
    st.markdown(
        """
            <span class="brand-title">StreetBase</span>
        </div>
        """,
        unsafe_allow_html=True
    )


def render_hero_section():
    # Anchor that our CSS targets; the NEXT horizontal block (columns) becomes the card
    st.markdown('<div id="hero-card-anchor"></div>', unsafe_allow_html=True)

    col_left, col_right = st.columns([2.5, 1], gap="large")

    with col_left:
        st.title("AI-Powered Real Estate Valuation")
        st.write("""
        Predicting house prices is complex, influenced by location, size, rooms, and economic conditions. 
        StreetBase uses *supervised machine learning* to accurately predict property values 
        based on historical data, providing valuable insights into housing price estimation.
        """)
        st.markdown("""
        <ul>
            <li>✨ <b>Real-time AI valuation</b> using regression models</li>
            <li>🚀 Built on <b>supervised ML</b> (Scikit-learn + Pandas)</li>
            <li>💡 Insights into <b>key factors</b> influencing property prices</li>
            <li>📊 Trained on comprehensive <b>Indian real estate data</b></li>
        </ul>
        """, unsafe_allow_html=True)

        st.write("")
        button_col1, button_col2, _ = st.columns([0.8, 0.8, 2])
        with button_col1:
            if st.button("Try AI Valuation", type="primary"):
                st.balloons()
                st.info("Navigating to the AI Valuation form!")
        with button_col2:
            if st.button("View Insights", type="secondary"):
                st.success("Displaying market insights!")

    with col_right:
        st.markdown(
            """
            <div class="quick-insights-box">
                <h2>Quick Insights</h2>
                <ul class="insights-list">
                    <li>Fast & Accurate AI predictions</li>
                    <li>Beautiful UI built with Streamlit</li>
                    <li>Multiple ML algorithms evaluated</li>
                    <li>Comprehensive datasets from major Indian cities</li>
                    <li>Feature analysis for price factors</li>
                </ul>
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown("</div>", unsafe_allow_html=True)




def render_cta_banner():
    st.markdown(
        """
        <div class="cta-banner">
            <span class="emoji">🚀</span>
            <h2>Ready to Evaluate Your Property?</h2>
            <p>
                Get instant AI-powered property valuation based on location, size, amenities, and market trends.
                Our machine learning model analyzes multiple factors to provide accurate price estimates.
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )


# --- Main App Execution ---
# --- Main App Execution ---
if __name__ == "__main__":
    custom_css_injection() # Apply our custom styles first

    render_brand_header() # Logo and SmartBricks title
    render_hero_section() # Main hero content and quick insights
    render_cta_banner()   # Bottom call-to-action banner
    
    # Placeholder for other members' work (will also adopt the custom styles)
    st.markdown("<br><br>", unsafe_allow_html=True) # Add some vertical space
    

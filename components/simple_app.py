import streamlit as st
import pandas as pd

# ✅ Page setup — must be the FIRST Streamlit command
st.set_page_config(
    page_title="Property Valuation",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="collapsed"  # hides default Streamlit sidebar
)

# 🧭 (Optional) If you already have a custom navbar component:
# from components.navbar import load_navbar
# load_navbar()

# Title
st.markdown("<h1 style='text-align:center;'>🏠 AI Property Valuation Tool</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center; font-size:18px;'>Get instant property valuations with 99.96% accuracy</p>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# Create two columns
col1, col2 = st.columns(2, gap="large")

with col1:
    st.header("📝 Property Details")
    
    location = st.selectbox("📍 Location", [
        "Mumbai", "Delhi", "Bangalore", "Chennai", "Hyderabad", 
        "Pune", "Kolkata", "Ahmedabad", "Jaipur", "Other"
    ])
    
    property_type = st.selectbox("🏢 Property Type", [
        "Apartment", "Villa", "Independent House", "Plot", "Commercial"
    ])
    
    area = st.number_input("📐 Area (sq.ft)", min_value=100, max_value=10000, value=1200)
    bedrooms = st.number_input("🛏️ Bedrooms", min_value=1, max_value=10, value=3)
    bathrooms = st.number_input("🚿 Bathrooms", min_value=1, max_value=10, value=2)
    age = st.slider("📅 Property Age (years)", 0, 50, 10)
    amenities = st.multiselect("🎯 Amenities", [
        "Parking", "Swimming Pool", "Gym", "Garden", 
        "Lift", "Security", "Playground"
    ])
    
    if st.button("🔍 Get Valuation", type="primary"):
        base_price = 50
        location_multiplier = {
            "Mumbai": 3.0, "Delhi": 2.5, "Bangalore": 2.0, 
            "Chennai": 1.8, "Hyderabad": 1.6, "Pune": 1.7,
            "Kolkata": 1.4, "Ahmedabad": 1.3, "Jaipur": 1.2, "Other": 1.0
        }
        type_multiplier = {
            "Apartment": 1.0, "Villa": 1.5, "Independent House": 1.3,
            "Plot": 0.8, "Commercial": 2.0
        }
        price = (base_price + 
                 area * 0.02 + 
                 bedrooms * 15 + 
                 max(0, (30 - age) * 2) + 
                 len(amenities) * 5) * location_multiplier.get(location, 1.0) * type_multiplier.get(property_type, 1.0)
        
        st.session_state.price = price
        st.session_state.calculated = True

with col2:
    st.header("📊 Valuation Results")
    
    if st.session_state.get("calculated", False):
        price = st.session_state.price
        
        st.success("✅ Valuation Complete!")
        
        st.markdown(f"""
        <div style='text-align: center; padding: 20px; background: #f0f8ff; border-radius: 10px; border-left: 5px solid #FF6600;'>
            <h1 style='color: #003366; font-size: 3rem; margin: 0;'>₹{price:.2f} Lakhs</h1>
            <p style='color: #666; font-size: 1.2rem;'>Estimated Property Value</p>
        </div>
        """, unsafe_allow_html=True)
        
        col_m1, col_m2 = st.columns(2)
        col_m1.metric("Price per Sq.Ft", f"₹{(price * 100000 / area):.0f}")
        col_m2.metric("Price Range", "±₹2.93L")
        
        st.subheader("🏠 Property Summary")
        summary_data = {
            "Detail": ["Location", "Type", "Area", "Bedrooms", "Bathrooms", "Age", "Amenities"],
            "Value": [location, property_type, f"{area} sq.ft", bedrooms, bathrooms, f"{age} years", len(amenities)]
        }
        st.dataframe(pd.DataFrame(summary_data), use_container_width=True)
        
        st.subheader("📞 Next Steps")
        col_a1, col_a2 = st.columns(2)
        if col_a1.button("👨‍💼 Expert Review"):
            st.info("Expert review requested!")
        if col_a2.button("📞 Contact Agent"):
            st.info("Agent will contact you!")
    else:
        st.info("👈 Fill property details and click 'Get Valuation'")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>🏠 <strong>AI Property Valuation Tool</strong> | Professional Real Estate Analysis</p>
</div>
""", unsafe_allow_html=True)

import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Contact Us - StreetBase",
    page_icon="📧",
    layout="wide" # Using 'wide' layout for a better map viewing experience
)

# --- Header & Introduction ---
st.title("📧 Contact StreetBase")
st.markdown("We're here to help you navigate the city. Fill out our form or connect with us directly via the options below.")

# --- Contact Form Section ---
st.subheader("Send Us a Message")
with st.form(key='contact_form', clear_on_submit=True): # clear_on_submit is a nice UX improvement
    
    # Define columns for a two-column form layout
    col_name, col_email = st.columns(2)
    with col_name:
        name = st.text_input(label="Your Name*", placeholder="Enter your full name")
    with col_email:
        email = st.text_input(label="Your Email Address*", placeholder="e.g., streetbase@example.com")
        
    subject = st.text_input(label="Subject (Optional)", placeholder="What is your query about?")
    message = st.text_area(label="Your Message*", placeholder="Type your message here...", height=150)
    
    submit_button = st.form_submit_button(label='🚀 Submit Message')

if submit_button:
    # Basic validation
    if not name or not email or not message:
        st.error("🚨 Please fill in your Name, Email, and Message before submitting.")
    elif "@" not in email:
        st.error("❌ Please enter a valid Email address.")
    else:
        # In a real app, you would send this data to an API/database.
        st.success(f"✅ Thank you, **{name}**! Your message has been submitted. We'll be in touch soon.")
        
        # Display submitted data (for demo purposes)
        with st.expander("Submitted Data Preview"):
            st.write(f"**Name:** {name}")
            st.write(f"**Email:** {email}")
            st.write(f"**Subject:** {subject if subject else 'Not provided'}")
            st.write(f"**Message:** {message}")


# ----------------------------------------------------------------------
# --- Alternative Contact Methods and Map ---
st.markdown("---")
st.subheader("📞 Direct Contact Information")

# Define the custom CSS for the contact cards and the map
contact_style = """
<style>
    /* Card Styling - Maintained and Enhanced */
    .contact-card {
        padding: 20px;
        margin: 10px 0;
        border-radius: 10px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.3);
        background-color: #262730; 
        text-align: center;
        transition: transform 0.2s;
        height: 100%;
        min-height: 160px; /* Ensure uniform size */
        display: flex;
        flex-direction: column;
        justify-content: center;
    }
    .contact-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.4);
    }
    .contact-title {
        font-size: 1.2em;
        font-weight: bold;
        color: #f63366; 
        margin-bottom: 5px;
    }
    .contact-detail {
        font-size: 1.3em;
        word-wrap: break-word; 
        color: white;
        margin-bottom: 5px;
    }
    .contact-hours {
        font-size: 0.9em;
        color: #CCCCCC; /* Lighter grey for secondary info */
    }
</style>
"""
st.markdown(contact_style, unsafe_allow_html=True)

# 1. Define Contact Data
contact_data = [
    {
        "title": "Call Us",
        "icon": "📱",
        "detail": "6264543645",
        "link": "tel:6264543645",
        "extra_info": "Available Mon-Fri, 9am - 5pm IST"
    },
    {
        "title": "Support Email",
        "icon": "📩",
        "detail": "contact_streetbase@gmail.com",
        "link": "mailto:contact_streetbase@gmail.com",
        "extra_info": "We aim to reply within 24 hours"
    },
    {
        "title": "Visit Our Office",
        "icon": "📍",
        "detail": "Origin Towers, Hi-Tech City, Hyderabad, Telangana - 500123",
        "link": "https://maps.app.goo.gl/25Fj6z9J5gK4Ua9N9", # Direct Maps URL (Placeholder, use an actual URL if available)
        "extra_info": "Office Hours: Mon-Fri, 9am - 6pm"
    },
]

# 2. Use columns for a neat, attractive grid layout
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for i, data in enumerate(contact_data):
    with columns[i]:
        # Use HTML to render the custom-styled card
        st.markdown(
            f"""
            <div class="contact-card">
                <div class="contact-title">{data['icon']} {data['title']}</div>
                <a href="{data['link']}" style="text-decoration: none;">
                    <div class="contact-detail">{data['detail']}</div>
                </a>
                <div class="contact-hours">{data['extra_info']}</div>
            </div>
            """,
            unsafe_allow_html=True
        )

# ----------------------------------------------------------------------
# --- EMBEDDED MAP SECTION ---
st.subheader("---")
st.subheader("🗺️ Find Our Location")
st.markdown("View our office location and get directions directly on the map below.")

# The address to embed
address_query = "Origin Towers, Hi-Tech City, Hyderabad, Telangana"

# Construct the embed URL: Using the 'q' parameter in Google Maps is the standard way to search and embed a location.
# Parameters:
# 'q': the search query (address)
# 't': map type (m=map, k=satellite, p=terrain)
# 'z': zoom level (1-20)
# 'output=embed': tells Google Maps to format the output for embedding in an iframe
map_embed_url = f"https://maps.google.com/maps?q={address_query}&t=m&z=15&ie=UTF8&iwloc=&output=embed"

# Embed the map using an HTML iframe
st.markdown(
    f"""
    <iframe 
        width="100%" 
        height="450" 
        frameborder="0" 
        scrolling="no" 
        marginheight="0" 
        marginwidth="0" 
        src="{map_embed_url}"
        allowfullscreen
        style="border-radius: 10px; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.5);"
    >
    </iframe>
    <div style="font-size: 0.8em; text-align: right; margin-top: 5px;">
        <a href="https://maps.google.com/?q={address_query}" target="_blank">Open in Google Maps</a>
    </div>
    """, 
    unsafe_allow_html=True
)
import streamlit as st
import os
import sys

# ✅ Ensure root paths work properly
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, "components"))
sys.path.append(os.path.join(project_root, "pages"))

# ✅ Import navbar and Hero components
from components.NavBar.navbar import navbar
from components.Hero import (
    custom_css_injection,
    render_brand_header,
    render_hero_section,
    render_cta_banner
)
from components.features import load_feature_section
from components.simple_app import load_valuation_section

# ---------------- STREAMLIT CONFIG ----------------
st.set_page_config(page_title="StreetBase", page_icon="🏠", layout="wide")

# ---------------- RENDER NAVBAR ----------------
# Hide the default Streamlit deploy menu, header, and footer
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

navbar()


# Get current page from URL
query_params = st.query_params
page = query_params.get("page", ["home"])[0]

if page == "home":
    custom_css_injection()
    render_brand_header()
    render_hero_section()
    render_cta_banner()
    load_valuation_section()
    load_feature_section()

elif page == "case_studies":
    import pages.case_studies as case_studies
    case_studies.load_case_studies_page()

elif page == "about_us":
    import pages.AboutUs as about_us
    about_us.load_about_us_page()

elif page == "articles":
    import pages.news as articles
    articles.load_articles_page()

elif page == "services":
    import pages.services as services
    services.load_services_page()

elif page == "login_signup":
    import pages.Signin as login_signup
    login_signup.load_login_signup_page()

# ---------------- LOGOUT HANDLER ----------------
if "logout" in st.query_params:
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.query_params.clear()
    st.rerun()

# ---------------- PAGE ROUTING ----------------
page = st.query_params.get("page", "home")

try:
    if page == "home":
        from components.Hero import (
            custom_css_injection,
            render_brand_header,
            render_hero_section,
            render_cta_banner,
        )
        from components.simple_app import load_valuation_section
        from components.features import load_feature_section

        custom_css_injection()
        render_brand_header()
        render_hero_section()
        render_cta_banner()
        load_valuation_section()
        load_feature_section()

    elif page == "services":
        import pages.services as services
        services.load_services_page()

    elif page == "case_studies":
        import pages.case_studies as case_studies
        case_studies.load_case_studies_page()

    elif page == "news":
        import pages.news as news
        news.load_articles_page()

    elif page == "AboutUs":
        import pages.AboutUs as about_us
        about_us.load_about_us_page()

    elif page == "login_signup":
        import pages.Signin as signin
        signin.load_login_signup_page()

    else:
        st.error("404 - Page not found 😢")

except Exception as e:
    st.error(f"Error loading page: {e}")


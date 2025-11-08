
try:
    import streamlit as st
except Exception as e:
    raise ModuleNotFoundError(
        "The 'streamlit' package is required to run this app; install it with 'pip install streamlit' "
        "and ensure your virtual environment is activated."
    ) from e

import sys, os

# Ensure project root is on sys.path so local packages like 'pages' are resolvable
project_root = os.path.abspath(os.path.dirname(__file__))
sys.path.insert(0, project_root)
sys.path.append(os.path.join(project_root, 'components'))

from components.NavBar.navbar import navbar
from components.Hero import (
    custom_css_injection,
    render_brand_header,
    render_hero_section,
    render_cta_banner
)
from components.simple_app import load_valuation_section
from components.features import load_feature_section

# Set up
st.set_page_config(page_title="StreetBase", page_icon="🏠", layout="wide")
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

import streamlit as st
import time
import sys, os

# NO navbar() HERE

# --- DB Setup ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.auth_db import init_db, register_user, verify_user

query_params = st.query_params
if "logout" in query_params and query_params["logout"] == "true":
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.success("You have been logged out.")
    st.query_params.clear()
    st.rerun()

init_db()

def load_signin_page():
    
    st.markdown("""
    <style>
        .smartbricks-nav { display: none !important; }
    </style>
""", unsafe_allow_html=True)


    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "username" not in st.session_state:
        st.session_state.username = ""

    st.markdown("""
    <style>
        header, footer {visibility: hidden;}
        div.block-container {padding-top: 2rem;}
        .login-title {
            text-align: center;
            color: #FF6600;
            font-size: 1.6rem;
            font-weight: bold;
            margin-bottom: 1rem;
        }
    </style>
    """, unsafe_allow_html=True)

    if not st.session_state.logged_in:
        tabs = st.tabs(["🔐 Login", "🆕 Register"])

        with tabs[0]:
            st.markdown("<div class='login-title'>User Login</div>", unsafe_allow_html=True)
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")

            if st.button("Login"):
                if verify_user(username, password):
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success(f"Welcome {username} 👋")
                    st.query_params.clear()
                    st.query_params["page"] = "home"
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

        with tabs[1]:
            st.markdown("<div class='login-title'>Create Account</div>", unsafe_allow_html=True)
            new_user = st.text_input("Choose a username")
            new_pass = st.text_input("Choose a password", type="password")

            if st.button("Register"):
                if register_user(new_user, new_pass):
                    st.success("Registered! You can now log in.")
                else:
                    st.warning("Username already exists.")

    else:
        st.success(f"Logged in as: {st.session_state.username}")
        if st.button("Logout"):
            st.session_state.logged_in = False
            st.session_state.username = ""
            st.rerun()

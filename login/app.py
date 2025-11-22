import streamlit as st
import time
import sys, os

# --- Force include project root path ---
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(current_dir, os.pardir))
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

from utils.auth_db import init_db, register_user, verify_user


# Initialize DB
init_db()

st.set_page_config(page_title="Login | Business Website", page_icon="🔐", layout="centered")

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "username" not in st.session_state:
    st.session_state.username = ""

def logout_user():
    st.session_state.logged_in = False
    st.session_state.username = ""

# ---------- CSS ----------
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
        .stButton>button {
            background-color: #FF6600;
            color: white;
            border-radius: 10px;
            font-weight: 600;
            width: 100%;
            height: 2.5rem;
        }
    </style>
""", unsafe_allow_html=True)

# ---------- LOGIN / REGISTER ----------
if not st.session_state.logged_in:
    tabs = st.tabs(["🔐 Login", "🆕 Register"])

    with tabs[0]:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div class='login-title'>User Login</div>", unsafe_allow_html=True)

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            if verify_user(username, password):
                with st.spinner("Logging in..."):
                    time.sleep(1)
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success(f"Welcome {username} 👋")
                st.rerun()
            else:
                st.error("❌ Invalid username or password.")

        st.markdown("</div>", unsafe_allow_html=True)

    with tabs[1]:
        st.markdown("<div class='login-container'>", unsafe_allow_html=True)
        st.markdown("<div class='login-title'>Create Account</div>", unsafe_allow_html=True)

        new_user = st.text_input("Choose a username", key="reg_user")
        new_pass = st.text_input("Choose a password", type="password", key="reg_pass")

        if st.button("Register"):
            if register_user(new_user, new_pass):
                st.success("✅ Registered successfully! You can now log in.")
            else:
                st.warning("⚠️ Username already exists.")

        st.markdown("</div>", unsafe_allow_html=True)

else:
    st.success(f"✅ Logged in as: {st.session_state.username}")
    st.write("Welcome to your **Dashboard!** Here you can view personalized content.")
    st.markdown("---")

    if st.button("Logout"):
        logout_user()
        st.rerun()

import streamlit as st

def login_page():
    # Hide Streamlit default UI (optional)
    st.markdown("<style>#MainMenu, footer {visibility: hidden;}</style>", unsafe_allow_html=True)

    st.title("Login / Sign Up")

    # Create tabs
    tab1, tab2 = st.tabs(["Login", "Sign Up"])

    # ----- Login Tab -----
    with tab1:
        with st.form("login_form"):
            username = st.text_input("Username", key="login_user")
            password = st.text_input("Password", type="password", key="login_pass")
            login_submit = st.form_submit_button("Login")
            
            if login_submit:
                if username and password:
                    # Set session state
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.page = "home"
                    
                    # Redirect to home
                    st.experimental_rerun()
                else:
                    st.warning("Please enter username and password")

    # ----- Sign Up Tab -----
    with tab2:
        with st.form("signup_form"):
            new_user = st.text_input("New Username", key="signup_user")
            new_pass = st.text_input("New Password", type="password", key="signup_pass")
            signup_submit = st.form_submit_button("Sign Up")

            if signup_submit:
                if new_user and new_pass:
                    # You can save new users to a database here
                    st.success("Sign Up successful! Please login.")
                    st.session_state.page = "login"
                    st.experimental_rerun()
                else:
                    st.warning("Please enter username and password")

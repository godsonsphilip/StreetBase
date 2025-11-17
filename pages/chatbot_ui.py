import streamlit as st
from StreetBase_chatbot import init_bot, answer_query

def chatbot_popup():
    if "chunks" not in st.session_state:
        st.session_state.chunks, st.session_state.embeddings = init_bot()
        st.session_state.chat_history = []
        st.session_state.popup_open = False

    st.markdown("""
        <style>

        /* Floating Chat Bubble */
        #floating-chat-btn {
            position: fixed;
            bottom: 25px;
            right: 25px;
            z-index: 999999;
            background: #4A90E2;
            color: white;
            width: 70px;
            height: 70px;
            border-radius: 50%;
            font-size: 32px;
            display: flex;
            justify-content: center;
            align-items: center;
            cursor: pointer;
            box-shadow: 0px 4px 16px rgba(0,0,0,0.3);
        }

        /* Chat Popup */
        #chat-popup-box {
            position: fixed;
            bottom: 110px;
            right: 25px;
            width: 350px;
            max-height: 500px;
            background-color: #1e1e1e;
            color: white;
            padding: 15px;
            border-radius: 16px;
            box-shadow: 0px 4px 20px rgba(0,0,0,0.35);
            overflow-y: auto;
            z-index: 999998;
        }

        </style>
    """, unsafe_allow_html=True)

    bubble_placeholder = st.empty()

    with bubble_placeholder.container():
        st.markdown('<div id="floating-chat-btn">', unsafe_allow_html=True)
        if st.button("💬", key="floating_chat_button"):
            st.session_state.popup_open = True
        st.markdown("</div>", unsafe_allow_html=True)

    if st.session_state.popup_open:

        popup_placeholder = st.empty()

        with popup_placeholder.container():
            st.markdown('<div id="chat-popup-box">', unsafe_allow_html=True)

            st.markdown("### StreetBase Chatbot")

            if st.button(" Close", key="close_btn"):
                st.session_state.popup_open = False
                st.rerun()

            for sender, msg in st.session_state.chat_history:
                st.chat_message("user" if sender=="user" else "assistant").markdown(msg)

            user_query = st.chat_input("Ask something about the PDF")

            if user_query:
                st.session_state.chat_history.append(("user", user_query))
                reply = answer_query(
                    user_query,
                    st.session_state.chunks,
                    st.session_state.embeddings
                )
                st.session_state.chat_history.append(("assistant", reply))
                st.rerun()

            st.markdown("</div>", unsafe_allow_html=True)

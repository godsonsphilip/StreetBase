import streamlit as st
import streamlit.components.v1 as components
from components.StreetBase_chatbot import init_bot, answer_query
# If your imports need to be relative, use:
# from .StreetBase_chatbot import init_bot, answer_query


def chatbot_popup():
    """
    Simple Streamlit chat wired to StreetBase bot.

    Behaviour:
    - Uses native st.chat_message + st.chat_input
    - Shows the small chat bar / icon near the footer (Streamlit default)
    - After sending a message, the page auto-scrolls down to the latest chat
    """

    # 1. One-time backend init
    if "chatbot_initialized" not in st.session_state:
        st.session_state.chunks, st.session_state.embeddings = init_bot()
        st.session_state.chat_history = []
        st.session_state.chatbot_initialized = True

    # Optional anchor for scroll targeting (not strictly needed but nice)
    st.markdown('<div id="streetbase-chat-anchor"></div>', unsafe_allow_html=True)

    # 2. Show existing chat history
    for sender, msg in st.session_state.chat_history:
        role = "user" if sender == "user" else "assistant"
        st.chat_message(role).markdown(msg)

    # 3. Native Streamlit chat input at the bottom
    user_query = st.chat_input("Ask StreetBase anything...")

    if user_query:
        # Save user message
        st.chat_message("user").markdown(user_query)
        st.session_state.chat_history.append(("user", user_query))

        # Get reply from your PDF-based chatbot
        reply = answer_query(
            user_query,
            st.session_state.chunks,
            st.session_state.embeddings,
        )

        st.chat_message("assistant").markdown(reply)
        st.session_state.chat_history.append(("assistant", reply))

        # Mark that we just added a new message
        st.session_state["_scroll_to_chat"] = True

    # 4. Auto-scroll to the latest chat message (or anchor)
    if st.session_state.get("_scroll_to_chat", False) or st.session_state.chat_history:
        # Once we've decided to scroll, clear the flag (so it doesn't lock you forever)
        st.session_state["_scroll_to_chat"] = False

        components.html(
            """
            <script>
            const streamlitDoc = window.parent.document;

            // Try to scroll to the last chat message
            const msgs = streamlitDoc.querySelectorAll('div[data-testid="stChatMessage"]');
            if (msgs.length > 0) {
                const lastMsg = msgs[msgs.length - 1];
                lastMsg.scrollIntoView({ behavior: "smooth", block: "end" });
            } else {
                // Fallback: scroll to our anchor, if present
                const anchor = streamlitDoc.getElementById("streetbase-chat-anchor");
                if (anchor) {
                    anchor.scrollIntoView({ behavior: "smooth", block: "end" });
                }
            }
            </script>
            """,
            height=0,
            width=0,
        )

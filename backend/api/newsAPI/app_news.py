import streamlit as st
from news_api import fetch_india_real_estate_news
from components import news_card, extract_tags
from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=60000, limit=None, key="real_estate_refresh")

st.title("🏡 Indian Real Estate News")
st.write("Latest housing, property, and real-estate market updates in India.")

if "articles" not in st.session_state:
    st.session_state.articles = None

if st.button("Fetch Latest News"):
    with st.spinner("Fetching real estate news from India..."):
        st.session_state.articles = fetch_india_real_estate_news()

if st.session_state.articles is None:
    st.stop()

articles = st.session_state.articles

if not articles:
    st.warning("No real estate news found right now.")
    st.stop()


st.subheader("🔎 Search & Filter")

search_query = st.text_input("Search articles…", "")

tag_set = set()
for a in articles:
    tag_set.update(extract_tags(a))
tag_list = sorted(list(tag_set))

selected_tags = st.multiselect("Filter by category:", tag_list)


filtered = articles.copy()

if search_query.strip():
    q = search_query.lower()
    filtered = [
        a for a in filtered
        if q in a["title"].lower() or q in a["description"].lower()
    ]

if selected_tags:
    filtered = [
        a for a in filtered
        if any(t in extract_tags(a) for t in selected_tags)
    ]
    
st.subheader(f"📰 Showing {len(filtered)} articles")

if not filtered:
    st.warning("No matching articles.")
else:
    for a in filtered:
        news_card(a)

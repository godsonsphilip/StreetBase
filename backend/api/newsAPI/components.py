import streamlit as st
from datetime import datetime, timezone
from urllib.parse import urlparse

def get_domain(url):
    try:
        net = urlparse(url).netloc.replace("www.", "")
        return net
    except:
        return "Unknown"

def human_time(utc_string):
    try:
        dt = datetime.strptime(utc_string, "%Y%m%dT%H%M%SZ")
        dt = dt.replace(tzinfo=timezone.utc)
        now = datetime.now(timezone.utc)
        diff = now - dt
        s = diff.total_seconds()

        if s < 60: return "Just now"
        if s < 3600: return f"{int(s//60)} minutes ago"
        if s < 86400: return f"{int(s//3600)} hours ago"
        if s < 172800: return "Yesterday"
        return f"{int(s//86400)} days ago"

    except:
        return utc_string

def extract_tags(article):
    text = (article.get("title") or "").lower()

    tags = []
    if "price" in text or "market" in text:
        tags.append("📈 Market")
    if "construction" in text or "infrastructure" in text:
        tags.append("🏗️ Construction")
    if "rent" in text or "rental" in text:
        tags.append("💸 Rental")
    if "housing" in text or "apartment" in text:
        tags.append("🏙️ Housing")
    if "loan" in text or "emi" in text or "mortgage" in text:
        tags.append("💰 Finance")

    if not tags:
        tags.append("📰 News")

    return tags

def news_card(article):

    st.markdown("""
        <style>
        .news-card {
            background: #111115;
            padding: 20px;
            border-radius: 16px;
            margin-bottom: 30px;
            border: 1px solid rgba(255,255,255,0.08);
            transition: transform 0.2s ease, box-shadow 0.2s ease;
        }
        .news-card:hover {
            transform: translateY(-4px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.4);
        }
        .news-title {
            font-size: 22px;
            font-weight: 700;
            margin-bottom: 8px;
            line-height: 1.35;
        }
        .news-meta {
            font-size: 14px;
            opacity: 0.75;
            margin-bottom: 12px;
        }
        .tag {
            display: inline-block;
            background: rgba(255,255,255,0.08);
            padding: 4px 10px;
            border-radius: 8px;
            margin-right: 6px;
            font-size: 12px;
        }
        </style>
    """, unsafe_allow_html=True)

    domain = get_domain(article["url"])
    seen_human = human_time(article.get("seendate", ""))
    tags = extract_tags(article)

    with st.container():
        st.markdown('<div class="news-card">', unsafe_allow_html=True)

        col1, col2 = st.columns([1.2, 2.5], gap="large")

        with col1:
            if article.get("image"):
                st.image(article["image"], use_container_width=True)
            else:
                st.image("https://i.imgur.com/3ZqXq5f.jpeg", use_container_width=True)

        with col2:
            st.markdown(f"<div class='news-title'>{article['title']}</div>", unsafe_allow_html=True)
            st.markdown(
                f"<div class='news-meta'>{domain} • {seen_human}</div>",
                unsafe_allow_html=True
            )

            # Tags
            tag_html = "".join([f"<span class='tag'>{t}</span>" for t in tags])
            st.markdown(tag_html, unsafe_allow_html=True)

            desc = article.get("description", "")
            if len(desc) > 220:
                desc = desc[:220].rstrip() + "…"

            st.write(desc)
            st.markdown(
                f"<a href='{article['url']}' target='_blank' style='font-size:15px;'>🔗 Read full article</a>",
                unsafe_allow_html=True
            )

        st.markdown("</div>", unsafe_allow_html=True)

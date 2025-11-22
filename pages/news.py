# main_app.py  (replace your current main file with this)
import streamlit as st  # pyright: ignore[reportMissingImports]
import pandas as pd
from datetime import datetime, timedelta, timezone
from components.NavBar.navbar import navbar # pyright: ignore[reportMissingImports]
import requests
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os
from urllib.parse import urlparse

# Auto-refresh
from streamlit_autorefresh import st_autorefresh

# Page configuration
st.set_page_config(page_title="News & Articles", layout="wide")

# Show navbar if you have it
navbar()

# --- Configuration ---
API_KEY = "d4d290fde3d8464b8d689e5726ebfd45"
BASE_URL = "https://newsapi.org/v2/everything"
DEFAULT_QUERY = "real estate india"
MODEL_PATH = "news_classifier_model.joblib"

# Define the set of all possible categories
ALL_CATEGORIES = [
    "Apartments",
    "Villas",
    "Market Trends",
    "Investment Tips",
    "Regulations",
    "Industry News"  # Default/Catch-all
]
REAL_ESTATE_KEYWORDS = [
    "real estate", "property", "housing", "apartment", "apartments",
    "rental", "rent", "construction", "infrastructure",
    "home", "homes", "flat", "flats", "land", "plot", "plots",
    "builder", "builders", "realty", "estate", "market",
    "prices", "mortgage", "loan", "housing loan", "emi"
]

INDIA_KEYWORDS = [
    "india", "indian", "delhi", "mumbai",
    "bangalore", "hyderabad", "pune", "chennai",
]

def is_indian(text):
    t = text.lower()
    return any(k in t for k in INDIA_KEYWORDS)

def is_real_estate(text):
    t = text.lower()
    return any(k in t for k in REAL_ESTATE_KEYWORDS)

def is_relevant_article(article):
    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "")
    ).lower()

    return is_indian(text) and is_real_estate(text)


# --- ML Model Setup (Mock Training) ---
def train_and_save_model():
    """Trains a simple Naive Bayes classifier and saves it."""
    X_train = [
        "New high-rise apartment project launched in Mumbai", "flat for sale in Delhi", "condo prices rising",
        "Luxury villa sales hit record high in Goa", "independent house for rent", "mansion tax implications",
        "Indian real estate market poised for growth", "economic forecast for housing sector", "property price trend",
        "Top investment tips for first-time homebuyers", "maximizing ROI on rental property", "equity investment strategy",
        "RERA regulation changes announced", "new tax policy for property transactions", "land law updates",
        "General news about the real estate industry", "developer announces new project", "construction update"
    ]
    y_train = [
        "Apartments", "Apartments", "Apartments",
        "Villas", "Villas", "Villas",
        "Market Trends", "Market Trends", "Market Trends",
        "Investment Tips", "Investment Tips", "Investment Tips",
        "Regulations", "Regulations", "Regulations",
        "Industry News", "Industry News", "Industry News"
    ]

    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    joblib.dump(model, MODEL_PATH)
    return model

# Load or train the model
if os.path.exists(MODEL_PATH):
    try:
        classifier = joblib.load(MODEL_PATH)
    except Exception:
        classifier = train_and_save_model()
else:
    classifier = train_and_save_model()

def ml_categorize_article(article_text):
    """Uses the trained ML model to predict the primary category."""
    predicted_category = classifier.predict([article_text])[0]
    return [predicted_category]


# -----------------------
# Helper utilities added
# -----------------------
def get_domain(url):
    try:
        net = urlparse(url).netloc.replace("www.", "")
        return net or "Unknown"
    except Exception:
        return "Unknown"

def human_time_from_iso(iso_string):
    """Convert ISO-8601 datetime to human-friendly relative time."""
    try:
        # handle common formats
        dt = None
        try:
            dt = datetime.fromisoformat(iso_string.replace("Z", "+00:00"))
        except Exception:
            # fallback for other formats
            dt = datetime.strptime(iso_string[:19], "%Y-%m-%dT%H:%M:%S").replace(tzinfo=timezone.utc)

        now = datetime.now(tz=timezone.utc)
        diff = now - dt.astimezone(timezone.utc)
        s = diff.total_seconds()

        if s < 60:
            return "Just now"
        if s < 3600:
            return f"{int(s // 60)} minutes ago"
        if s < 86400:
            return f"{int(s // 3600)} hours ago"
        if s < 172800:
            return "Yesterday"
        return f"{int(s // 86400)} days ago"
    except Exception:
        return iso_string

def extract_tags(article):
    """Return small set of emoji-prefixed tags based on title/description."""
    text = ((article.get("title") or "") + " " + (article.get("description") or "")).lower()
    tags = []
    if any(k in text for k in ["price", "market", "prices", "trend"]):
        tags.append("📈 Market")
    if any(k in text for k in ["construction", "infrastructure", "build", "project"]):
        tags.append("🏗️ Construction")
    if any(k in text for k in ["rent", "rental", "lease", "tenant"]):
        tags.append("💸 Rental")
    if any(k in text for k in ["housing", "apartment", "flat", "homes"]):
        tags.append("🏙️ Housing")
    if any(k in text for k in ["loan", "emi", "mortgage", "tax", "finance", "investment", "roi"]):
        tags.append("💰 Finance")

    if not tags:
        tags.append("📰 News")
    return tags

# --- Data Fetching ---
def get_news_data(query: str, page_size: int = 50):
    params = {
        "q": query,
        "language": "en",
        "sortBy": "publishedAt",
        "apiKey": API_KEY,
        "pageSize": page_size
    }

    articles_data = []

    try:
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()
        news = response.json().get("articles", [])

        for i, item in enumerate(news):

            published_at = item.get("publishedAt") or datetime.now(timezone.utc).isoformat()
            content_for_categorization = f"{item.get('title', '')} {item.get('description', '')}"

            articles_data.append({
                "id": i + 1,
                "title": item.get("title", "No Title"),
                "description": item.get("description", "No Description Available"),
                "publishedAt": published_at,
                "date": None,
                "author": item.get("author", "Unknown"),
                "image_url": item.get("urlToImage") or "https://via.placeholder.com/500x300.png?text=Real+Estate+News",
                "url": item.get("url", "#"),
                "content_text": content_for_categorization,
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "popularity_score": i + 1
            })

    except Exception as e:
        st.error(f"⚠️ Failed to fetch real-time articles: {e}. Showing demo content instead.")
        articles_data = [
            # fallback data...
        ]

    # ✅ APPLY FILTER HERE, AFTER FETCHING
    articles_data = [
        a for a in articles_data
        if is_relevant_article(a)
    ]

    return articles_data


def categorize_articles(articles):
    """Assigns articles to categories using the ML model and popularity."""
    categorized_news = {
        "Trending": [],
        "Most Read": [],
    }
    for cat in ALL_CATEGORIES:
        categorized_news[cat] = []

    for article in articles:
        # Use the ML model for primary categorization
        ml_categories = ml_categorize_article(article["content_text"])
        article["categories"] = ml_categories

        # Populate Trending and Most Read (using popularity_score)
        if article.get("popularity_score", 9999) <= 10:
            categorized_news["Trending"].append(article)
        if article.get("popularity_score", 9999) <= 5:
            categorized_news["Most Read"].append(article)

        for cat in ml_categories:
            if cat in categorized_news:
                categorized_news[cat].append(article)
            else:
                categorized_news.setdefault(cat, []).append(article)

    # Remove duplicates within each category
    for category in list(categorized_news.keys()):
        unique_articles = {a['id']: a for a in categorized_news[category]}.values()
        categorized_news[category] = list(unique_articles)

    # Remove empty categories
    categorized_news = {k: v for k, v in categorized_news.items() if v}
    return categorized_news

def render_article_card(article, is_featured=False):
    """Renders a single article card using HTML/Markdown but preserves your main theme."""
    card_class = "featured-article" if is_featured else "article-card"
    title_class = "featured-title" if is_featured else "article-title"
    desc_class = "featured-description" if is_featured else "article-description"

    # CSS: kept your gradient/theme but add small tag & meta styling
    st.markdown("""
        <style>
        .article-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 15px;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        .article-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 12px rgba(0, 0, 0, 0.2);
        }
        .article-title {
            color: white;
            font-size: 18px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .article-title a { color: white; text-decoration: none; }
        .article-title a:hover { text-decoration: underline; }
        .article-description {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .article-meta {
            color: rgba(255,255,255,0.85);
            font-size: 13px;
            margin-bottom: 8px;
        }
        .article-category {
            display: inline-block;
            background-color: rgba(255, 255, 255, 0.18);
            color: white;
            padding: 4px 10px;
            border-radius: 20px;
            font-size: 12px;
            margin-right: 8px;
            margin-top: 5px;
        }
        .featured-article {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            padding: 30px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.15);
        }
        .featured-title { color: white; font-size: 28px; font-weight: bold; margin-bottom: 15px; }
        .featured-description { color: rgba(255,255,255,0.95); font-size: 16px; line-height:1.8; margin-bottom:15px; }

        /* small tag chips inspired by the second file but matching main theme */
        .tag-chip {
            display:inline-block;
            background: rgba(255,255,255,0.12);
            color: #fff;
            padding: 6px 10px;
            border-radius: 12px;
            margin-right:6px;
            font-size:12px;
        }
        div[data-testid="stVerticalBlock"] > .featured-article,
        div[data-testid="stHorizontalBlock"] > .featured-article {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%) !important;
        }

        div[data-testid="stVerticalBlock"],
        div[data-testid="stHorizontalBlock"] {
            background: transparent !important;
        }
        .featured-article:not(.featured-article) {
            background: none !important;
        }
        </style>
    """, unsafe_allow_html=True)

    # Domain + human time + tags
    domain = get_domain(article.get("url", "#"))
    human_published = human_time_from_iso(article.get("publishedAt", datetime.now(timezone.utc).isoformat()))
    tags = extract_tags(article)

    # Build HTML card (keeps original look but adds image, time, domain, small tag chips)
    image_url = article.get("image_url") or article.get("urlToImage") or "https://via.placeholder.com/500x300.png?text=News"
    title_html = f'<div class="{title_class}"><a href="{article["url"]}" target="_blank">{article["title"]}</a></div>'
    meta_html = f'<div class="article-meta">{domain} • {human_published} • By <strong>{article.get("author","Unknown")}</strong></div>'
    tag_html = "".join([f'<span class="tag-chip">{t}</span>' for t in tags])

    # Truncate description
    desc = article.get("description", "") or ""
    if len(desc) > 220:
        desc = desc[:220].rstrip() + "…"

    # Render as columns keeping your layout
    st.markdown(f'<div class="{card_class}">', unsafe_allow_html=True)
    cols = st.columns([1.2, 2.5], gap="large")
    with cols[0]:
        try:
            st.image(image_url, use_container_width=True)
        except Exception:
            st.image("https://via.placeholder.com/500x300.png?text=News", use_container_width=True)

    with cols[1]:
        st.markdown(title_html, unsafe_allow_html=True)
        st.markdown(meta_html, unsafe_allow_html=True)
        st.markdown(tag_html, unsafe_allow_html=True)
        st.write(desc)
        st.markdown(
            f"<a href='{article.get('url','')}' target='_blank' style='font-size:15px; color:white; font-weight:600;'>🔗 Read full article →</a>",
            unsafe_allow_html=True
        )

    st.markdown("</div>", unsafe_allow_html=True)


# --- Page ----
def load_articles_page():
    """Load and display the articles page"""

    # auto refresh every 60 seconds (60000 ms). Using st_autorefresh to reload the page.
    st_autorefresh(interval=60000, limit=None, key="real_estate_refresh")

    # Page title
    st.title("📰 Real Estate News & Articles")
    st.markdown("Stay updated with the latest trends, insights, and news in the real estate industry.")

    # --- Search Bar (Prominent placement) ---
    search_query = st.text_input(
        "Search all news articles...",
        placeholder="e.g., 'new apartment regulations' or 'villa investment'",
        key="main_search_box"
    )
    st.markdown("---")

    # --- Fetch and Categorize Data ---
    fetch_query = search_query.strip() if search_query.strip() else DEFAULT_QUERY

    # Fetch a larger set of articles to ensure good categorization
    articles_data = get_news_data(query=fetch_query, page_size=50)

    # Client-side additional filtering: If user typed something, prefer to filter local results by title+description
    if search_query.strip():
        q = search_query.lower()
        filtered_local = [
            a for a in articles_data
            if q in (a.get("title") or "").lower() or q in (a.get("description") or "").lower()
        ]
        # If local filtering yields results, use them; otherwise keep the API results (avoid empty UI)
        if filtered_local:
            articles_data = filtered_local

    # Categorize the fetched articles
    categorized_news = categorize_articles(articles_data)

    # --- Display Categorized Sections ---

    # Featured Article (use the most recent/popular from the entire set)
    if articles_data:
        featured = articles_data[0]
        st.subheader("🔥 Featured Article")
        render_article_card(featured, is_featured=True)
        st.markdown("---")

    # Display all categories
    for category, articles in categorized_news.items():
        if articles:
            st.header(f"🗞️ {category} ({len(articles)})")

            with st.expander(f"View {len(articles)} articles in {category}", expanded=category in ["Trending", "Most Read"]):
                cols_per_row = 2
                for i in range(0, len(articles), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(articles):
                            article = articles[i + j]
                            with col:
                                render_article_card(article, is_featured=False)
            st.markdown("---")

    if not articles_data:
        st.info("📭 No articles found. Please try a different search query.")

    # Newsletter
    st.subheader("📧 Subscribe to Our Newsletter")
    col1, col2 = st.columns([3, 1])
    with col1:
        email = st.text_input("Enter your email to get weekly real estate news", key="newsletter_email")
    with col2:
        if st.button("Subscribe", key="newsletter_subscribe"):
            if email:
                st.success(f"✅ Subscribed! You'll receive updates at {email}")
            else:
                st.error("Please enter a valid email address")

# Run the page function
if __name__ == "__main__":
    load_articles_page()

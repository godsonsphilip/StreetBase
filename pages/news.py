import streamlit as st# pyright: ignore[reportMissingImports] 
import pandas as pd
from datetime import datetime, timedelta
from components.NavBar.navbar import navbar# pyright: ignore[reportMissingImports] 
import requests
import re 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline
import joblib
import os

# Page configuration
# st.set_page_config(page_title="News & Articles", layout="wide")

# Display navbar


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
    "Industry News" # Default/Catch-all
]

# --- ML Model Setup (Mock Training) ---
# In a real application, this would be pre-trained on a large dataset.
# Here, we mock a simple training process for demonstration.
def train_and_save_model():
    """Trains a simple Naive Bayes classifier and saves it."""
    
    # Simplified training data
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
    
    # Create a pipeline: TF-IDF Vectorizer -> Multinomial Naive Bayes Classifier
    model = make_pipeline(TfidfVectorizer(), MultinomialNB())
    model.fit(X_train, y_train)
    
    # Save the model
    joblib.dump(model, MODEL_PATH)
    return model

# Load or train the model
if os.path.exists(MODEL_PATH):
    try:
        classifier = joblib.load(MODEL_PATH)
    except Exception:
        # Fallback to training if loading fails
        classifier = train_and_save_model()
else:
    classifier = train_and_save_model()

def ml_categorize_article(article_text):
    """Uses the trained ML model to predict the primary category."""
    
    # Predict the category
    predicted_category = classifier.predict([article_text])[0]
    
    # For a more robust display, we can return the predicted category and a few others
    # For simplicity, we'll just return the single best prediction as a list
    return [predicted_category]

# --- Data Fetching ---
def get_news_data(query: str, page_size: int = 50):
    """Fetches news articles from NewsAPI."""
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
            content_for_categorization = f"{item.get('title', '')} {item.get('description', '')}"
            
            articles_data.append({
                "id": i + 1,
                "title": item.get("title", "No Title"),
                "description": item.get("description", "No Description Available"),
                "date": datetime.strptime(item.get("publishedAt", datetime.now().isoformat())[:10], "%Y-%m-%d"),
                "author": item.get("author", "Unknown"),
                "image_url": item.get("urlToImage") or "https://via.placeholder.com/500x300.png?text=Real+Estate+News",
                "url": item.get("url", "#"),
                "content_text": content_for_categorization,
                "source": item.get("source", {}).get("name", "Unknown Source"),
                "popularity_score": i + 1 
            })
    except Exception as e:
        st.error(f"⚠️ Failed to fetch real-time articles: {e}. Showing demo content instead.")
        # Fallback to demo content
        articles_data = [
            {"id": 1, "title": "Indian Real Estate Market Poised for Growth", "description": "Experts predict a surge in real estate demand.", "date": datetime.now() - timedelta(days=3), "author": "The Realty Journal", "url": "#", "content_text": "market trend growth", "source": "Journal", "popularity_score": 1},
            {"id": 2, "title": "Luxury Villa Sales Hit Record High", "description": "High-net-worth individuals are investing in villas.", "date": datetime.now() - timedelta(days=7), "author": "Housing Today", "url": "#", "content_text": "villa luxury home investment", "source": "Housing", "popularity_score": 2},
            {"id": 3, "title": "New Apartment Project Launched in Mumbai", "description": "Affordable flats are now available for booking.", "date": datetime.now() - timedelta(days=1), "author": "Mumbai News", "url": "#", "content_text": "apartment flat mumbai", "source": "Mumbai News", "popularity_score": 3},
        ]
        
    return articles_data

def categorize_articles(articles):
    """Assigns articles to categories using the ML model and popularity."""
    
    # 1. Initialize categories
    categorized_news = {
        "Trending": [],
        "Most Read": [], 
    }
    
    # Initialize all other categories
    for cat in ALL_CATEGORIES:
        categorized_news[cat] = []
    
    # 2. Assign articles to ML-based categories
    for article in articles:
        # Use the ML model for primary categorization
        ml_categories = ml_categorize_article(article["content_text"])
        
        # The ML model returns a list of categories (even if it's just one)
        article["categories"] = ml_categories
        
        # 3. Populate Trending and Most Read (using popularity_score as a proxy)
        # Trending: Top 10 most recent/popular
        if article["popularity_score"] <= 10:
            categorized_news["Trending"].append(article)
            
        # Most Read: Top 5 most recent/popular 
        if article["popularity_score"] <= 5:
            categorized_news["Most Read"].append(article)
            
        # 4. Populate ML-based categories
        for cat in ml_categories:
            if cat in categorized_news:
                categorized_news[cat].append(article)
            else:
                # Handle dynamic categories if the ML model were more complex
                # For this mock, we stick to ALL_CATEGORIES
                if cat not in categorized_news:
                    categorized_news[cat] = []
                categorized_news[cat].append(article)

    # Remove duplicates within each category (based on article ID)
    for category in categorized_news:
        unique_articles = {a['id']: a for a in categorized_news[category]}.values()
        categorized_news[category] = list(unique_articles)
        
    # Remove empty categories
    categorized_news = {k: v for k, v in categorized_news.items() if v}
        
    return categorized_news

def render_article_card(article, is_featured=False):
    """Renders a single article card using HTML/Markdown."""
    
    # Determine CSS class for styling
    card_class = "featured-article" if is_featured else "article-card"
    title_class = "featured-title" if is_featured else "article-title"
    desc_class = "featured-description" if is_featured else "article-description"
    
    # Generate category tags
    category_tags = "".join([f'<span class="article-category">{cat}</span>' for cat in article.get("categories", ["News"])])
    
    return f"""
        <div class="{card_class}">
            <div class="{title_class}"><a href="{article['url']}" target="_blank">{article['title']}</a></div>
            <div class="{desc_class}">{article['description']}</div>
            <div style="color: rgba(255, 255, 255, 0.8); margin-bottom: 10px;">
                By <strong>{article['author']}</strong> | {article['date'].strftime('%B %d, %Y')}
            </div>
            <div>{category_tags}</div>
            <a href="{article['url']}" target="_blank" style="
                display:inline-block;
                margin-top:10px;
                padding:8px 15px;
                background-color:white;
                color:#f5576c;
                font-weight:600;
                text-decoration:none;
                border-radius:6px;
            ">Read Full Article →</a>
        </div>
    """

def load_articles_page():
    """Load and display the articles page"""

    # Page title
    st.title("📰 Real Estate News & Articles")
    st.markdown("Stay updated with the latest trends, insights, and news in the real estate industry.")

    # --- CSS Styling ---
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
        .article-title a {
            color: white;
            text-decoration: none;
        }
        .article-title a:hover {
            text-decoration: underline;
        }
        .article-date {
            color: rgba(255, 255, 255, 0.7);
            font-size: 12px;
            margin-bottom: 8px;
        }
        .article-description {
            color: rgba(255, 255, 255, 0.9);
            font-size: 14px;
            line-height: 1.6;
            margin-bottom: 10px;
        }
        .article-category {
            display: inline-block;
            background-color: rgba(255, 255, 255, 0.2);
            color: white;
            padding: 4px 12px;
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
        .featured-title {
            color: white;
            font-size: 28px;
            font-weight: bold;
            margin-bottom: 15px;
        }
        .featured-description {
            color: rgba(255, 255, 255, 0.95);
            font-size: 16px;
            line-height: 1.8;
            margin-bottom: 15px;
        }
        </style>
    """, unsafe_allow_html=True)

    # --- Search Bar (Prominent placement) ---
    search_query = st.text_input(
        "Search all news articles...", 
        placeholder="e.g., 'new apartment regulations' or 'villa investment'", 
        key="main_search_box"
    )
    st.markdown("---")

    # --- Fetch and Categorize Data ---
    # Use the main search query if provided, otherwise use the default query
    fetch_query = search_query if search_query else DEFAULT_QUERY
    
    # Fetch a larger set of articles to ensure good categorization
    articles_data = get_news_data(query=fetch_query, page_size=50)
    
    # Categorize the fetched articles
    categorized_news = categorize_articles(articles_data)
    
    # --- Display Categorized Sections ---
    
    # 1. Featured Article (The most recent/popular from the entire set)
    if articles_data:
        featured = articles_data[0]
        st.subheader("🔥 Featured Article")
        st.markdown(render_article_card(featured, is_featured=True), unsafe_allow_html=True)
        st.markdown("---")

    # 2. Display all categories
    for category, articles in categorized_news.items():
        if articles:
            st.header(f"🗞️ {category} ({len(articles)})")
            
            # Use a Streamlit expander for cleaner layout
            with st.expander(f"View {len(articles)} articles in {category}", expanded=category in ["Trending", "Most Read"]):
                
                # Display articles in a 2-column grid
                cols_per_row = 2
                for i in range(0, len(articles), cols_per_row):
                    cols = st.columns(cols_per_row)
                    for j, col in enumerate(cols):
                        if i + j < len(articles):
                            article = articles[i + j]
                            with col:
                                # Render the card, but not as featured inside the category section
                                st.markdown(render_article_card(article, is_featured=False), unsafe_allow_html=True)
            st.markdown("---")
            
    if not articles_data:
        st.info("📭 No articles found. Please try a different search query.")

    # --- Newsletter (Kept from original code) ---
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
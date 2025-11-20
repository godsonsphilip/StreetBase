import requests
import html
from bs4 import BeautifulSoup
from urllib.parse import urlparse


REAL_ESTATE_KEYWORDS = [
    "real estate", "property", "housing", "apartment", "apartments",
    "rental", "rent", "construction", "infrastructure",
    "home", "homes", "flat", "flats", "land", "plot", "plots",
    "builder", "builders", "realty", "estate", "market",
    "prices", "mortgage", "loan", "housing loan", "emi"
]

INDIA_KEYWORDS = ["india", "indian", "delhi", "mumbai", "bangalore", "hyderabad", "pune", "chennai"]

FALLBACK_IMAGE = "https://i.imgur.com/3ZqXq5f.jpeg"  


def safe_json(response):
    try:
        return response.json()
    except Exception:
        return {}


def fetch_og_image(url):
    """Try to extract the OG image from the article page."""
    try:
        html_page = requests.get(url, timeout=5).text
        soup = BeautifulSoup(html_page, "html.parser")
        og = soup.find("meta", property="og:image")
        if og and og.get("content"):
            return og["content"]
    except:
        pass
    return None


def is_indian(text):
    text = text.lower()
    return any(k in text for k in INDIA_KEYWORDS)


def is_relevant(article):
    text = (
        (article.get("title") or "") + " " +
        (article.get("description") or "") + " " +
        (article.get("url") or "")
    ).lower()

    if not is_indian(text):
        return False

    return any(k in text for k in REAL_ESTATE_KEYWORDS)


def fetch_url(url):
    r = requests.get(url)
    return safe_json(r).get("articles", [])


def fetch_india_real_estate_news():

    urls = [
        "https://api.gdeltproject.org/api/v2/doc/doc?query=title:india AND (real estate OR property OR housing OR apartment OR rental OR construction)&mode=artlist&maxrecords=50&format=json&sort=datedesc",
        "https://api.gdeltproject.org/api/v2/doc/doc?query=india real estate housing property apartment construction&mode=artlist&maxrecords=50&format=json&sort=datedesc",
        "https://api.gdeltproject.org/api/v2/doc/doc?query=india housing market prices&mode=artlist&maxrecords=50&format=json&sort=datedesc"
    ]

    raw_articles = []
    for u in urls:
        raw_articles.extend(fetch_url(u))

    if not raw_articles:
        return []

    cleaned = []
    seen = set()

    for item in raw_articles:
        url = item.get("url", "")
        if url in seen:
            continue
        seen.add(url)

        article = {
            "title": html.unescape(item.get("title", "No title")),
            "source": get_source(item),        
            "url": url,
            "image": None,
            "description": item.get("description") or item.get("seendate", ""),
            "seendate": item.get("seendate", "")
        }


        if not is_relevant(article):
            continue

        gdelt_img = item.get("image")
        if gdelt_img and gdelt_img.startswith("http"):
            article["image"] = gdelt_img
        else:
            og_img = fetch_og_image(url)
            if og_img:
                article["image"] = og_img
            else:
                article["image"] = FALLBACK_IMAGE

        cleaned.append(article)

    return cleaned

def get_source(item):
    if item.get("domain"):
        return item["domain"]

    if item.get("sourceurl"):
        parsed = urlparse(item["sourceurl"])
        return parsed.netloc.replace("www.", "")

    if item.get("url"):
        parsed = urlparse(item["url"])
        return parsed.netloc.replace("www.", "")

    return "Unknown"

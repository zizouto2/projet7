import requests
import re

from app.config import settings

# Liste optimisée (extrait des 100 actifs les plus populaires, tu peux l’étendre)
POPULAR_STOCKS = {
    "apple", "tesla", "amazon", "google", "microsoft", "meta", "nvidia", "berkshire", "visa",
    "jpmorgan", "johnson & johnson", "walmart", "mastercard", "exxon", "procter & gamble",
    "chevron", "pepsico", "coca cola", "disney", "paypal", "intel", "ibm", "netflix",
    "salesforce", "qualcomm", "boeing", "adobe", "oracle", "nike", "mcdonald's", "starbucks",
    "shell", "unilever", "alibaba", "samsung", "toyota", "honda", "sony", "lenovo", "snap",
    "uber", "lyft", "airbnb", "zoom", "block", "at&t", "verizon", "intel", "amd", "arm",
    "spotify", "shopify", "coinbase", "robinhood", "binance", "byd", "baidu", "pinduoduo",
    "xpeng", "nio", "lucid", "ford", "gm", "stellantis", "volkswagen", "bmw", "mercedes",
    "revolut", "stripe", "snowflake", "palantir", "tencent", "jd.com", "gameStop", "amc",
    "kraft", "3m", "caterpillar", "abbvie", "bristol-myers", "moderna", "pfizer", "novartis",
    "sanofi", "gsk", "lvmh", "hermes", "kering", "total", "airbus", "safran", "engie",
    "orange", "bnp paribas", "societe generale", "credit agricole", "axa", "renault", "stellantis"
}

def is_off_topic(question: str) -> bool:
    off_topic_keywords = ["recette", "cuisine", "jardinage", "voyage", "météo"]
    return any(keyword in question.lower() for keyword in off_topic_keywords)

def is_current_event_question(question: str) -> bool:
    keywords = ["actualité", "news", "dernier", "aujourd'hui", "breaking", "récemment"]
    return any(keyword in question.lower() for keyword in keywords)

def detect_stock_names(text: str) -> list[str]:
    text_lower = text.lower()
    return [name.title() for name in POPULAR_STOCKS if name in text_lower]

def perform_targeted_search(query: str, num_results: int = 3) -> list[dict]:
    if not settings.serpapi_key:
        return []

    search_query = f"{query} site:bloomberg.com OR site:investing.com"
    params = {
        "engine": "google",
        "q": search_query,
        "api_key": settings.serpapi_key,
        "num": num_results
    }
    try:
        response = requests.get("https://serpapi.com/search", params=params)
        results = response.json().get("organic_results", [])
    except Exception as e:
        print(f"Erreur SerpAPI : {e}")
        return []

    filtered = []
    for r in results:
        link = r.get("link", "")
        if "bloomberg.com" in link or "investing.com" in link:
            filtered.append({
                "title": r.get("title", ""),
                "snippet": r.get("snippet", ""),
                "link": link
            })
        if len(filtered) >= num_results:
            break

    return filtered

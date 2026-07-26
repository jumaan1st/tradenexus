import requests
import config


def fetch_news(query, country=None, language=None):
    """Fetch news headlines via SerpAPI."""
    country = country or config.NEWS_COUNTRY
    language = language or config.NEWS_LANGUAGE

    url = "https://serpapi.com/search"
    params = {
        "engine": "google_news",
        "q": query,
        "gl": country.lower(),
        "hl": language,
        "api_key": config.SERPAPI_KEY,
        "num": config.NEWS_ARTICLE_COUNT
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("news_results", [])

    news = []
    for item in results[:config.NEWS_ARTICLE_COUNT]:
        title = item.get("title")
        link = item.get("link")
        source = item.get("source", {}).get("name")
        date = item.get("date")
        news.append(f"Title: {title}\nDate: {date}\nLink: {link}\nSource: {source}\n")
    return news if news else ["No news found."]

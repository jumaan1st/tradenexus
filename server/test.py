import requests

def get_news_via_serpapi(query, api_key, country="IN", language="en"):
    url = "https://serpapi.com/search"
    params = {
        "engine": "google_news",
        "q": query,
        "gl": country.lower(),
        "hl": language,
        "api_key": api_key,
        "num": 10
    }
    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()
    results = data.get("news_results", [])  # (check actual key in response)
    news = []
    for item in results[:10]:
        title = item.get("title")
        link  = item.get("link")
        source = item.get("source", {}).get("name")
        date = item.get("date")
        news.append(f"📰 {title}\n📅 {date}\n🔗 {link}\nSource: {source}\n")
    return news if news else ["No news found."]

# Usage:
api_key = "e75208e44369759b6f4edb19573d25b5099a1810d39460010304b81dd65546b1"
news = get_news_via_serpapi("Google stock", api_key, country="IN", language="en")
print("\n".join(news))
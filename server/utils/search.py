import requests
import urllib.parse
import config


def fetch_first_url(query, api_key=None):
    """Search via SearchAPI and return the first organic result URL."""
    api_key = api_key or config.SEARCHAPI_KEY
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and "organic_results" in data:
        return data["organic_results"][0]["link"]
    else:
        print("Error fetching data:", data.get("error", "Unknown error"))
        return None


def get_ticker(comp_name):
    """Resolve a company name to its Yahoo Finance ticker symbol."""
    query = f"{comp_name} Yahoo Finance"
    first_result = fetch_first_url(query)
    ticker_symbol = first_result.split('/')[4]
    return urllib.parse.unquote(ticker_symbol)

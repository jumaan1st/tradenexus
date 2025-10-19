from googlesearch import search
import urllib.parse
import requests

def fetch_first_url(query, api_key):
    url = "https://www.searchapi.io/api/v1/search"
    params = {
        "engine": "google",
        "q": query,
        "api_key": api_key
    }
    response = requests.get(url, params=params)
    data = response.json()

    if response.status_code == 200 and "organic_results" in data:
        first_url = data["organic_results"][0]["link"]
        return first_url
    else:
        print("Error fetching data:", data.get("error", "Unknown error"))
        return None


def get_ticker(comp_name):
    query = f"{comp_name} Yahoo Finance"
    first_result = fetch_first_url(query, "zeUH2nsjXf3q853aE8ee6pet")
    ticker_symbol = first_result.split('/')[4]
    
    return urllib.parse.unquote(ticker_symbol)


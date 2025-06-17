from googlesearch import search
import urllib.parse
def get_ticker(comp_name):
    query = f"{comp_name} Yahoo Finance"
    first_result = next(search(query, num_results=1), None)
    ticker_symbol = first_result.split('/')[4]
    
    return urllib.parse.unquote(ticker_symbol)


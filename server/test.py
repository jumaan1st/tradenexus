from yahooquery import search

def get_ticker_symbol(company_name):
    results = search(company_name)
    print(f"Search results for '{company_name}': {results}")

get_ticker_symbol("Apple Inc yahoo finance")  # Example usage, replace with actual company name
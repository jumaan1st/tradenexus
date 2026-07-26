import requests
import pandas as pd
from bs4 import BeautifulSoup


def scrape_market_data(url, element_id, table_limit=None):
    """Scrape market data tables from Moneycontrol."""
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    gain_loss = soup.find(id=element_id)
    if not gain_loss:
        return None

    tables = gain_loss.find_all("table")
    if table_limit:
        tables = tables[:table_limit]

    all_tables_json = []
    for table in tables:
        df = pd.read_html(str(table))[0]
        all_tables_json.append(df.to_dict(orient='records'))

    return all_tables_json

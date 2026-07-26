from decimal import Decimal, ROUND_HALF_UP
import requests
import yfinance as yf


def get_stock_price_in_inr(symbol, use_current_price, user_price=None):
    """Fetch stock price and convert to INR if necessary. Returns (price, name)."""
    stock = yf.Ticker(symbol)
    info = stock.info

    if use_current_price:
        price = Decimal(str(info['regularMarketPrice']))
        currency = info['currency']
        if currency != "INR":
            response = requests.get(
                f"https://api.frankfurter.app/latest?amount={price}&from={currency}&to=INR"
            )
            fx_data = response.json()
            if 'rates' not in fx_data:
                raise ValueError("Currency conversion failed")
            price = Decimal(str(fx_data['rates']['INR'])).quantize(
                Decimal("0.01"), rounding=ROUND_HALF_UP
            )
    else:
        if user_price is None:
            raise ValueError("Purchase price required when currentPrice is False")
        price = Decimal(str(user_price))

    return price, info['shortName']


def convert_to_inr(price, currency):
    """Convert a price from given currency to INR."""
    if currency == "INR":
        return price
    response = requests.get(
        f"https://api.frankfurter.app/latest?amount={price}&from={currency}&to=INR"
    )
    fx_data = response.json()
    if 'rates' not in fx_data:
        raise ValueError("Currency conversion failed")
    return Decimal(str(fx_data['rates']['INR'])).quantize(
        Decimal("0.01"), rounding=ROUND_HALF_UP
    )

import pandas as pd
import yfinance as yf
import feedparser
from googlesearch import search
import urllib.parse
from flask import jsonify, request

def analyze_stock(comp_name, data=None):
    """
    Fetches stock data using yfinance, performs technical and fundamental analysis,
    and retrieves news headlines for a given company.

    Args:
        comp_name (str): Name of the company.
        data (dict, optional): Pre-fetched stock data. If None, data is fetched from yfinance.

    Returns:
        dict: Combined stock data and analysis results.
    """
    # ----------- Fetch Stock Data -----------
    if data is None:
        ticker_symbol = None
        try:
            # Search for ticker symbol via Yahoo Finance
            query = f"Yahoo Finance {comp_name}"
            first_result = next(search(query, num_results=1))
            ticker_symbol = first_result.split('/')[4]
            ticker_symbol = urllib.parse.unquote(ticker_symbol)  # Decode URL-encoded ticker symbol
            stock = yf.Ticker(ticker_symbol)

            # Fetch stock info and history
            info = stock.info
            history = stock.history(period="2mo")
            currency = info.get('currency', 'USD')

            if history.empty or len(history) < 20:
                raise ValueError("Insufficient historical data for analysis (minimum 20 days required).")

            # Structure the data
            data = {
                "company_name": info.get('longName', 'N/A'),
                "market_cap": info.get('marketCap', 'N/A'),
                "eps": info.get('trailingEps', 'N/A'),
                "revenue": info.get('totalRevenue', 'N/A'),
                "revenue_growth": info.get('revenueGrowth', 'N/A'),
                "pe_ratio": info.get('trailingPE', 'N/A'),
                "de_ratio": info.get('debtToEquity', 'N/A'),
                "roe": info.get('returnOnEquity', 'N/A'),
                "div_yield": info.get('dividendYield', 'N/A'),
                "history": history.reset_index().to_dict(orient="records"),
            }
        except Exception as e:
            raise ValueError(f"Error fetching data for {comp_name}: {str(e)}")

    # ----------- Prepare DataFrames -----------
    df = pd.DataFrame(data['history'])[['Date', 'Close', 'Volume']]
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df = df.tail(20).reset_index(drop=True)

    # ----------- Technical Indicators -----------
    current_price = df['Close'].iloc[-1]
    sma_5 = df['Close'].rolling(5).mean().iloc[-1]
    sma_10 = df['Close'].rolling(10).mean().iloc[-1]

    def compute_rsi(series, period=14):
        delta = series.diff().dropna()
        gain = delta.where(delta > 0, 0.0)
        loss = -delta.where(delta < 0, 0.0)
        avg_gain = gain.head(period).mean()
        avg_loss = loss.head(period).mean()
        for i in range(period, len(gain)):
            avg_gain = (avg_gain * (period - 1) + gain.iloc[i]) / period
            avg_loss = (avg_loss * (period - 1) + loss.iloc[i]) / period
        rs = avg_gain / (avg_loss + 1e-10)
        return 100 - (100 / (1 + rs))

    rsi = compute_rsi(df['Close'])

    ema12 = df['Close'].ewm(span=12, adjust=False).mean()
    ema26 = df['Close'].ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26
    signal = macd.ewm(span=9, adjust=False).mean()
    macd_value = macd.iloc[-1]
    signal_value = signal.iloc[-1]

    momentum = current_price - df['Close'].iloc[-11] if len(df) >= 11 else 0
    price_trend = current_price - df['Close'].iloc[0]
    volume_trend = "Increasing" if df['Volume'].iloc[-1] > df['Volume'].rolling(5).mean().iloc[-1] else "Decreasing"
    daily_returns = df['Close'].pct_change()
    volatility = daily_returns.std() * 100 * (252 ** 0.5)

    def generate_technical_verdict(sma_5, sma_10, rsi, macd, signal, momentum, price_trend, volume_trend, volatility):
        score = 0
        if rsi > 50: score += 1
        if macd > signal: score += 1
        if momentum > 0: score += 1
        if volume_trend == "Increasing": score += 1
        if sma_5 > sma_10: score += 1
        if price_trend > 0: score += 1

        if rsi < 30:
            return "Buy - Oversold"
        elif rsi > 70:
            return "Sell - Overbought"
        elif volatility > 30:
            return "Caution - High Volatility"
        elif score >= 4:
            return "Buy - Strong Bullish Indicators"
        elif score <= 1:
            return "Sell - Strong Bearish Indicators"
        else:
            return "Hold - Mixed Signals"

    technical_verdict = generate_technical_verdict(
        sma_5, sma_10, rsi, macd_value, signal_value, momentum, price_trend, volume_trend, volatility
    )

    # ----------- Fundamental Analysis -----------
    def safe_float(value):
        try:
            return float(value) if value != 'N/A' else None
        except (ValueError, TypeError):
            return None

    eps = safe_float(data['eps'])
    revenue_growth = safe_float(data['revenue_growth'])
    pe_ratio = safe_float(data['pe_ratio'])
    de_ratio = safe_float(data['de_ratio'])
    roe = safe_float(data['roe'])
    div_yield = safe_float(data['div_yield'])

    def generate_fundamental_verdict(eps, revenue_growth, pe_ratio, de_ratio, roe, div_yield):
        score = 0
        if eps is not None and eps > 0: score += 1
        if revenue_growth is not None and revenue_growth > 0.05: score += 1
        if pe_ratio is not None and 10 <= pe_ratio <= 25: score += 1
        if de_ratio is not None and de_ratio < 1: score += 1
        if roe is not None and roe > 0.15: score += 1
        if div_yield is not None and div_yield > 0.02: score += 1

        if score >= 5:
            return "Buy - Strong Fundamentals"
        elif score >= 3:
            return "Hold - Moderately Strong"
        else:
            return "Sell - Weak Fundamentals"

    fundamental_verdict = generate_fundamental_verdict(
        eps, revenue_growth, pe_ratio, de_ratio, roe, div_yield
    )

    # ----------- News Headlines -----------
    def get_google_news_headlines(query):
        try:
            query = query.replace(' ', '+')
            url = f"https://news.google.com/rss/search?q={query}"
            feed = feedparser.parse(url)
            news = []
            for entry in feed.entries[:15]:  # Limit to top 5 headlines
                title = entry.title
                published = entry.published
                news.append(f"📰 {title}\n📅 {published}\n")
            # url = f"https://news.google.com/rss/search?q=global Stock Market News {query}"
            # feed = feedparser.parse(url)
            # global_news = []
            # for entry in feed.entries[:15]:  # Limit to top 5 headlines
            #     title = entry.title
            #     published = entry.published
            #     news.append(f"📰 {title}\n📅 {published}\n")
            return news
        except Exception:
            return ["Unable to fetch news headlines."]

    news = get_google_news_headlines(f"{comp_name} Stocks latest info")

    # ----------- Return Combined Results -----------
    return {
        "stock_name": ticker_symbol if ticker_symbol else comp_name,
        "stock_data": data,
        "currency": currency,
        "technical_analysis": {
            "verdict": technical_verdict,
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2),
            "macd": round(macd_value, 2),
            "signal": round(signal_value, 2),
            "momentum": round(momentum, 2),
            "price_trend": round(price_trend, 2),
            "volume_trend": volume_trend,
            "volatility": round(volatility, 2),
            "sma_5": round(sma_5, 2),
            "sma_10": round(sma_10, 2)
        },
        "fundamental_analysis": {
            "verdict": fundamental_verdict,
            "eps": eps if eps is not None else 'N/A',
            "revenue_growth": revenue_growth if revenue_growth is not None else 'N/A',
            "pe_ratio": pe_ratio if pe_ratio is not None else 'N/A',
            "de_ratio": de_ratio if de_ratio is not None else 'N/A',
            "roe": roe if roe is not None else 'N/A',
            "div_yield": div_yield if div_yield is not None else 'N/A'
        },
        "news_headlines": news
    }
import pandas as pd
import yfinance as yf
import urllib.parse

from utils.search import fetch_first_url
from services.news import fetch_news
import config


def _safe_float(value):
    try:
        return float(value) if value != 'N/A' else None
    except (ValueError, TypeError):
        return None


def _compute_rsi(series, period=None):
    period = period or config.RSI_PERIOD
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


def _technical_verdict(sma_short, sma_long, rsi, macd, signal, momentum, price_trend, volume_trend, volatility):
    score = 0
    if rsi > config.RSI_NEUTRAL: score += 1
    if macd > signal: score += 1
    if momentum > 0: score += 1
    if volume_trend == "Increasing": score += 1
    if sma_short > sma_long: score += 1
    if price_trend > 0: score += 1

    if rsi < config.RSI_OVERSOLD:
        return "Buy - Oversold"
    elif rsi > config.RSI_OVERBOUGHT:
        return "Sell - Overbought"
    elif volatility > config.HIGH_VOLATILITY_THRESHOLD:
        return "Caution - High Volatility"
    elif score >= config.BULLISH_SCORE_THRESHOLD:
        return "Buy - Strong Bullish Indicators"
    elif score <= config.BEARISH_SCORE_THRESHOLD:
        return "Sell - Strong Bearish Indicators"
    else:
        return "Hold - Mixed Signals"


def _fundamental_verdict(eps, revenue_growth, pe_ratio, de_ratio, roe, div_yield):
    score = 0
    if eps is not None and eps > 0: score += 1
    if revenue_growth is not None and revenue_growth > config.REVENUE_GROWTH_THRESHOLD: score += 1
    if pe_ratio is not None and config.PE_RATIO_MIN <= pe_ratio <= config.PE_RATIO_MAX: score += 1
    if de_ratio is not None and de_ratio < config.DE_RATIO_MAX: score += 1
    if roe is not None and roe > config.ROE_THRESHOLD: score += 1
    if div_yield is not None and div_yield > config.DIV_YIELD_THRESHOLD: score += 1

    if score >= config.STRONG_FUNDAMENTALS_SCORE:
        return "Buy - Strong Fundamentals"
    elif score >= config.MODERATE_FUNDAMENTALS_SCORE:
        return "Hold - Moderately Strong"
    else:
        return "Sell - Weak Fundamentals"


def _fetch_stock_data(comp_name):
    """Fetch raw stock data from Yahoo Finance via SearchAPI ticker lookup."""
    query = f"Yahoo Finance {comp_name}"
    first_result = fetch_first_url(query)
    ticker_symbol = urllib.parse.unquote(first_result.split('/')[4])
    stock = yf.Ticker(ticker_symbol)
    info = stock.info
    history = stock.history(period=config.STOCK_HISTORY_PERIOD)
    currency = info.get('currency', 'USD')

    if history.empty or len(history) < config.STOCK_MIN_HISTORY_DAYS:
        raise ValueError("Insufficient historical data for analysis.")

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
    return ticker_symbol, currency, data


def analyze_stock(comp_name, data=None):
    """Full stock analysis: technical + fundamental + news."""
    ticker_symbol = None
    currency = "USD"

    if data is None:
        ticker_symbol, currency, data = _fetch_stock_data(comp_name)

    df = pd.DataFrame(data['history'])[['Date', 'Close', 'Volume']]
    df['Date'] = pd.to_datetime(df['Date'])
    df.sort_values('Date', inplace=True)
    df = df.tail(config.STOCK_ANALYSIS_WINDOW).reset_index(drop=True)

    # Technical indicators
    current_price = df['Close'].iloc[-1]
    sma_short = df['Close'].rolling(config.SMA_SHORT).mean().iloc[-1]
    sma_long = df['Close'].rolling(config.SMA_LONG).mean().iloc[-1]
    rsi = _compute_rsi(df['Close'])

    ema_short = df['Close'].ewm(span=config.EMA_SHORT, adjust=False).mean()
    ema_long = df['Close'].ewm(span=config.EMA_LONG, adjust=False).mean()
    macd = ema_short - ema_long
    signal = macd.ewm(span=config.MACD_SIGNAL, adjust=False).mean()
    macd_value = macd.iloc[-1]
    signal_value = signal.iloc[-1]

    lookback = config.MOMENTUM_LOOKBACK + 1
    momentum = current_price - df['Close'].iloc[-lookback] if len(df) >= lookback else 0
    price_trend = current_price - df['Close'].iloc[0]
    volume_trend = (
        "Increasing" if df['Volume'].iloc[-1] > df['Volume'].rolling(config.VOLUME_ROLLING_PERIOD).mean().iloc[-1]
        else "Decreasing"
    )
    daily_returns = df['Close'].pct_change()
    volatility = daily_returns.std() * 100 * (config.TRADING_DAYS_PER_YEAR ** 0.5)

    technical = _technical_verdict(
        sma_short, sma_long, rsi, macd_value, signal_value, momentum, price_trend, volume_trend, volatility
    )

    # Fundamental analysis
    eps = _safe_float(data['eps'])
    revenue_growth = _safe_float(data['revenue_growth'])
    pe_ratio = _safe_float(data['pe_ratio'])
    de_ratio = _safe_float(data['de_ratio'])
    roe = _safe_float(data['roe'])
    div_yield = _safe_float(data['div_yield'])

    fundamental = _fundamental_verdict(eps, revenue_growth, pe_ratio, de_ratio, roe, div_yield)

    # News
    news = fetch_news(f"{comp_name} Stocks latest info")

    return {
        "stock_name": ticker_symbol if ticker_symbol else comp_name,
        "stock_data": data,
        "currency": currency,
        "technical_analysis": {
            "verdict": technical,
            "current_price": round(current_price, 2),
            "rsi": round(rsi, 2),
            "macd": round(macd_value, 2),
            "signal": round(signal_value, 2),
            "momentum": round(momentum, 2),
            "price_trend": round(price_trend, 2),
            "volume_trend": volume_trend,
            "volatility": round(volatility, 2),
            "sma_5": round(sma_short, 2),
            "sma_10": round(sma_long, 2)
        },
        "fundamental_analysis": {
            "verdict": fundamental,
            "eps": eps if eps is not None else 'N/A',
            "revenue_growth": revenue_growth if revenue_growth is not None else 'N/A',
            "pe_ratio": pe_ratio if pe_ratio is not None else 'N/A',
            "de_ratio": de_ratio if de_ratio is not None else 'N/A',
            "roe": roe if roe is not None else 'N/A',
            "div_yield": div_yield if div_yield is not None else 'N/A'
        },
        "news_headlines": news
    }

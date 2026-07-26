import os
from dotenv import load_dotenv

load_dotenv()

# --- API Keys ---
SEARCHAPI_KEY = os.environ.get("SEARCHAPI_KEY")
SERPAPI_KEY = os.environ.get("SERPAPI_KEY")
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# --- AI Provider ---
AI_PROVIDER = os.environ.get("AI_PROVIDER", "gemini")
AI_MODEL = os.environ.get("AI_MODEL")
OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "llama3.1")
DEEPSEEK_API_KEY = os.environ.get("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.environ.get("DEEPSEEK_BASE_URL", "https://api.deepseek.com")

# --- Stock Data ---
STOCK_HISTORY_PERIOD = os.environ.get("STOCK_HISTORY_PERIOD", "2mo")
STOCK_MIN_HISTORY_DAYS = int(os.environ.get("STOCK_MIN_HISTORY_DAYS", "20"))
STOCK_ANALYSIS_WINDOW = int(os.environ.get("STOCK_ANALYSIS_WINDOW", "20"))

# --- Technical Indicator Periods ---
RSI_PERIOD = int(os.environ.get("RSI_PERIOD", "14"))
SMA_SHORT = int(os.environ.get("SMA_SHORT", "5"))
SMA_LONG = int(os.environ.get("SMA_LONG", "10"))
EMA_SHORT = int(os.environ.get("EMA_SHORT", "12"))
EMA_LONG = int(os.environ.get("EMA_LONG", "26"))
MACD_SIGNAL = int(os.environ.get("MACD_SIGNAL", "9"))
MOMENTUM_LOOKBACK = int(os.environ.get("MOMENTUM_LOOKBACK", "10"))
TRADING_DAYS_PER_YEAR = int(os.environ.get("TRADING_DAYS_PER_YEAR", "252"))
VOLUME_ROLLING_PERIOD = int(os.environ.get("VOLUME_ROLLING_PERIOD", "5"))

# --- RSI Thresholds ---
RSI_OVERSOLD = float(os.environ.get("RSI_OVERSOLD", "30"))
RSI_NEUTRAL = float(os.environ.get("RSI_NEUTRAL", "50"))
RSI_OVERBOUGHT = float(os.environ.get("RSI_OVERBOUGHT", "70"))

# --- Volatility Threshold ---
HIGH_VOLATILITY_THRESHOLD = float(os.environ.get("HIGH_VOLATILITY_THRESHOLD", "30"))

# --- Technical Score Thresholds ---
BULLISH_SCORE_THRESHOLD = int(os.environ.get("BULLISH_SCORE_THRESHOLD", "4"))
BEARISH_SCORE_THRESHOLD = int(os.environ.get("BEARISH_SCORE_THRESHOLD", "1"))

# --- Fundamental Analysis Thresholds ---
REVENUE_GROWTH_THRESHOLD = float(os.environ.get("REVENUE_GROWTH_THRESHOLD", "0.05"))
PE_RATIO_MIN = float(os.environ.get("PE_RATIO_MIN", "10"))
PE_RATIO_MAX = float(os.environ.get("PE_RATIO_MAX", "25"))
DE_RATIO_MAX = float(os.environ.get("DE_RATIO_MAX", "1"))
ROE_THRESHOLD = float(os.environ.get("ROE_THRESHOLD", "0.15"))
DIV_YIELD_THRESHOLD = float(os.environ.get("DIV_YIELD_THRESHOLD", "0.02"))
STRONG_FUNDAMENTALS_SCORE = int(os.environ.get("STRONG_FUNDAMENTALS_SCORE", "5"))
MODERATE_FUNDAMENTALS_SCORE = int(os.environ.get("MODERATE_FUNDAMENTALS_SCORE", "3"))

# --- News ---
NEWS_ARTICLE_COUNT = int(os.environ.get("NEWS_ARTICLE_COUNT", "30"))
NEWS_COUNTRY = os.environ.get("NEWS_COUNTRY", "IN")
NEWS_LANGUAGE = os.environ.get("NEWS_LANGUAGE", "en")

# --- JWT ---
JWT_EXPIRY_DAYS = int(os.environ.get("JWT_EXPIRY_DAYS", "7"))

# --- Server ---
SERVER_HOST = os.environ.get("SERVER_HOST", "0.0.0.0")
SERVER_PORT = int(os.environ.get("SERVER_PORT", "5000"))
DEBUG_MODE = os.environ.get("DEBUG_MODE", "true").lower() == "true"

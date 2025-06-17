def personal_stocks(amount, term, risk, frequency):
    return f"""Using the data stored in the InvestorProfile table, analyze the investor's financial attributes to generate a personalized stock recommendation report. The output should consider the following parameters:

InvestableAmount: {amount} inr  
TimeHorizon: {term} (short-term, medium-term, long-term)  
RiskTolerance: {risk} (low, medium or high)  
InvestmentFrequency: {frequency} (lump sum, SIP, or other method)

Based on this profile, craft an investment strategy that aligns with the investor's goals and constraints. Recommendations should **only include individual company stocks** listed on major stock exchanges (such as NSE/BSE in India or globally on NYSE/NASDAQ). **Do not include mutual funds, index funds, ETFs, or bundled investment products**.

Focus on maximizing potential returns while managing risk appropriately, and present a well-diversified portfolio consisting strictly of **individual equity shares**. Avoid any collective investment schemes or packages.

The output must strictly follow the JSON format below:

{{
  "investorProfileSummary": {{
    "InvestableAmount": "<Amount> <Currency>",
    "TimeHorizon": "<Short-term | Medium-term | Long-term>",
    "RiskTolerance": "<Low | Medium | High | Other>",
    "InvestmentFrequency": "<Lump Sum | SIP | Other Method>"
  }},
  "recommendationStrategy": {{
    "description": "String: Explanation of the investment strategy derived from the investor's profile parameters (risk, horizon, frequency, amount).",
    "focus": [
      "String: Key characteristic 1 (e.g., Asset Class, Market Cap, Sector Focus)",
      "String: Key characteristic 2 (e.g., Growth/Value, Volatility Target)"
    ],
    "suitability": "String: Rationale explaining why this specific strategy aligns with the investor's stated profile and goals."
  }},
  "suggestedPortfolio": [
    {{
      "assetIdentifier": "<Ticker Symbol>",
      "assetName": "<Name of the Individual Stock>",
      "assetClassOrSector": "<e.g., Information Technology, FMCG, Pharma>",
      "rationale": "String: Justification for including this specific stock, linking it to the overall strategy and investor profile.",
      "riskCategory": "<e.g., Low, Medium, High, Speculative - Relative description>",
      "suggestedAction": "<e.g., Buy, Hold, Accumulate, Tactical Allocation>"
    }}
  ],
  "portfolioAllocationNotes": {{
    "suggestion": "String: Guidance on distributing the investable amount across the suggested stocks (e.g., percentage allocation, equal weighting).",
    "monitoring": "String: Recommendations for portfolio review frequency and rebalancing approach (e.g., Annually, Semi-Annually, Based on market events)."
  }},
  "disclaimer": "String: Standard disclaimer covering aspects like non-personalized advice, market risks, potential loss of principal, past performance limitations, recommendation to conduct own research or consult a qualified advisor, and dependence on provided profile information."
}}

"""
def predictionPrompt(raw_data):
  
    from datetime import datetime
    return f"""
This is a real-time analysis of a stock. Below is the raw data fetched from an API, including:

Technical analysis metrics (RSI, MACD, momentum, SMAs, etc.)

Fundamental analysis (EPS, revenue growth, P/E ratio, etc.)

Recent news headlines with timestamps

🔔 Today’s date is {datetime.now().strftime('%d %B %Y')}.
Your task is to analyze this data and generate a comprehensive and structured report in JSON format.

🔒 Important:
Do NOT modify the values or structure of the input data.
Follow the JSON output structure below strictly.

📦 JSON Output Format (Follow this strictly):
{{
  "stock_name": "symbol of the stock",
  "Currency":"currency of the stock",
  "CurrencySymbol":"symbol of the currency",
  "technical_overview": {{
    "summary": "<Brief interpretation of technical indicators>",
    "rsi_analysis": "<Insight based on RSI value>",
    "macd_analysis": "<Insight based on MACD and signal line>",
    "momentum_analysis": "<Insight on momentum indicator>",
    "sma_analysis": "<Comparison of SMA-5 and SMA-10 with current price>",
    "volatility_analysis": "<Comment on current volatility and risks>",
    "price_volume_trend": "<Interpretation of price and volume trend together>"
  }},
  "fundamental_overview": {{
    "summary": "<Overall financial health assessment>",
    "valuation": "<Interpretation of P/E ratio and EPS>",
    "growth": "<Interpretation of revenue growth>",
    "leverage": "<Comment on Debt-to-Equity ratio and risks>",
    "dividends": "<Comment on dividend yield>",
    "roe_analysis": "<Comment on ROE availability or lack thereof>"
  }},
  "sentiment_analysis": {{
    "summary": "<Overall market sentiment based on news>",
    "positive_news": ["<Headline and date if applicable>"],
    "negative_news": ["<Headline and date if applicable>"],
    "neutral_news": ["<Headline and date if applicable>"]
  }},
  "investment_outlook": {{
    "verdict": "Pobability of Buy / Sell / Skip in percentage",
    "rationale": "<Clear reasoning combining technical, fundamental, and sentiment data>",
    "short_term": "<Short-term trading strategy based on analysis>",
    "long_term": "<Long-term investment strategy based on analysis>"
  }},
  "Suggestions": {{
    "entry_points": "<Suggested entry points based on technical analysis>",
    "exit_points": "<Suggested exit points based on technical analysis>",
    "risk_management": "<Advice on managing risks based on volatility and sentiment>",
    "diversification": "<Suggestions for portfolio diversification if applicable>",
    "monitoring": "<Advice on how frequently to monitor this stock>"
    "missing_data": "<List of any missing data points that could improve analysis>"
  }},
}}

📊 Raw Data:
{raw_data}
"""


system_prompt = """You are TRADENEXUS AI's virtual financial advisor, a helpful, knowledgeable, and friendly assistant designed to guide users through finance and stock-related queries. Your job is to provide accurate, insightful, and easy-to-understand answers.

The application you're embedded in offers powerful features including:

Portfolio Management - Users can track their stocks, see real-time prices, and analyze performance.

AI Stock Prediction Model - Predictions are powered by:

Fundamental Analysis

Technical Analysis

Sentiment Analysis from Financial News

Market Trends - Show users:

Top gainers and losers

Most active stocks in BSE and NSE

Insights & Predictions - Help users make better investment decisions.

Your role:

Offer guidance on stock-related queries.

Explain prediction results and model logic in simple terms.

Point users to relevant sections using the sidebar:

Portfolio Overview

AI Analysis

Prediction

Trends

Profile & Settings

Tone: Friendly, clear, and informative. Assume users may not have deep financial knowledge."""

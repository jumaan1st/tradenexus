from datetime import datetime


def personal_stocks(amount, term, risk, frequency):
    prompt = f"""Using the data stored in the InvestorProfile table, analyze the investor's financial attributes to generate a personalized stock recommendation report. The output should consider the following parameters:

InvestableAmount: {amount} inr
TimeHorizon: {term} (short-term, medium-term, long-term)
RiskTolerance: {risk} (low, medium or high)
InvestmentFrequency: {frequency} (lump sum, SIP, or other method)

Based on this profile, craft an investment strategy that aligns with the investor's goals and constraints. Recommendations should **only include individual company stocks** listed on major stock exchanges (such as NSE/BSE in India or globally on NYSE/NASDAQ). **Do not include mutual funds, index funds, ETFs, or bundled investment products**.

Focus on maximizing potential returns while managing risk appropriately, and present a well-diversified portfolio consisting strictly of **individual equity shares**. Avoid any collective investment schemes or packages."""

    output_format = {
        "name": "stock_recommendation_report",
        "schema": {
            "type": "object",
            "properties": {
                "investorProfileSummary": {
                    "type": "object",
                    "properties": {
                        "InvestableAmount": {"type": "string"},
                        "TimeHorizon": {
                            "type": "string",
                            "enum": ["Short-term", "Medium-term", "Long-term"]
                        },
                        "RiskTolerance": {
                            "type": "string",
                            "enum": ["Low", "Medium", "High", "Other"]
                        },
                        "InvestmentFrequency": {
                            "type": "string",
                            "enum": ["Lump Sum", "SIP", "Other Method"]
                        }
                    },
                    "required": [
                        "InvestableAmount",
                        "TimeHorizon",
                        "RiskTolerance",
                        "InvestmentFrequency"
                    ],
                    "additionalProperties": False
                },
                "recommendationStrategy": {
                    "type": "object",
                    "properties": {
                        "description": {"type": "string"},
                        "focus": {
                            "type": "array",
                            "items": {"type": "string"}
                        },
                        "suitability": {"type": "string"}
                    },
                    "required": ["description", "focus", "suitability"],
                    "additionalProperties": False
                },
                "suggestedPortfolio": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "properties": {
                            "assetIdentifier": {"type": "string"},
                            "assetName": {"type": "string"},
                            "assetClassOrSector": {"type": "string"},
                            "rationale": {"type": "string"},
                            "riskCategory": {"type": "string"},
                            "suggestedAction": {
                                "type": "string",
                                "enum": ["Buy", "Hold", "Accumulate", "Tactical Allocation"]
                            }
                        },
                        "required": [
                            "assetIdentifier",
                            "assetName",
                            "assetClassOrSector",
                            "rationale",
                            "riskCategory",
                            "suggestedAction"
                        ],
                        "additionalProperties": False
                    }
                },
                "portfolioAllocationNotes": {
                    "type": "object",
                    "properties": {
                        "suggestion": {"type": "string"},
                        "monitoring": {"type": "string"}
                    },
                    "required": ["suggestion", "monitoring"],
                    "additionalProperties": False
                },
                "disclaimer": {"type": "string"}
            },
            "required": [
                "investorProfileSummary",
                "recommendationStrategy",
                "suggestedPortfolio",
                "portfolioAllocationNotes",
                "disclaimer"
            ],
            "additionalProperties": False
        }
    }

    return prompt, output_format


def prediction_prompt(raw_data):
    prompt = f"""
This is a real-time analysis of a stock. Below is the raw data fetched from an API, including:

Technical analysis metrics (RSI, MACD, momentum, SMAs, etc.)
Fundamental analysis (EPS, revenue growth, P/E ratio, etc.)
Recent news headlines with timestamps

Today's date is {datetime.now().strftime('%d %B %Y')}.
Your task is to analyze this data and generate a comprehensive and structured report.

Important:
Do NOT modify the values or structure of the input data.

Additionally, perform a basic Shariah (Halal) compliance screening for this stock based on
standard criteria used by Islamic finance screening methodologies (e.g. AAOIFI-style):
- Business activity: the company's core business must not be primarily involved in
  alcohol, gambling, conventional banking/insurance, pork products, adult entertainment,
  weapons, or other impermissible sectors.
- Financial ratios (if derivable from the provided data): interest-bearing debt to market
  cap, interest income to revenue, and illiquid assets to total assets should each
  generally stay below commonly used thresholds (e.g. ~33%).
If the raw data does not contain enough information to assess business activity or the
relevant financial ratios (e.g. no sector/industry classification, no debt or interest
income figures), classify the screening as "Cannot Determine" rather than guessing, and
state exactly what information is missing in the reasoning field.

Raw Data:
{raw_data}
"""

    output_format = {
        "name": "stock_prediction_report",
        "schema": {
            "type": "object",
            "properties": {
                "stock_name": {"type": "string", "description": "Symbol of the stock"},
                "Currency": {"type": "string", "description": "Currency of the stock"},
                "CurrencySymbol": {"type": "string", "description": "Symbol of the currency"},

                "technical_overview": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string", "description": "Brief interpretation of technical indicators"},
                        "rsi_analysis": {"type": "string", "description": "Insight based on RSI value"},
                        "macd_analysis": {"type": "string", "description": "Insight based on MACD and signal line"},
                        "momentum_analysis": {"type": "string", "description": "Insight on momentum indicator"},
                        "sma_analysis": {"type": "string",
                                         "description": "Comparison of SMA-5 and SMA-10 with current price"},
                        "volatility_analysis": {"type": "string",
                                                "description": "Comment on current volatility and risks"},
                        "price_volume_trend": {"type": "string",
                                               "description": "Interpretation of price and volume trend together"}
                    },
                    "required": [
                        "summary", "rsi_analysis", "macd_analysis",
                        "momentum_analysis", "sma_analysis",
                        "volatility_analysis", "price_volume_trend"
                    ],
                    "additionalProperties": False
                },

                "fundamental_overview": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string", "description": "Overall financial health assessment"},
                        "valuation": {"type": "string", "description": "Interpretation of P/E ratio and EPS"},
                        "growth": {"type": "string", "description": "Interpretation of revenue growth"},
                        "leverage": {"type": "string", "description": "Comment on Debt-to-Equity ratio and risks"},
                        "dividends": {"type": "string", "description": "Comment on dividend yield"},
                        "roe_analysis": {"type": "string", "description": "Comment on ROE availability or lack thereof"}
                    },
                    "required": [
                        "summary", "valuation", "growth",
                        "leverage", "dividends", "roe_analysis"
                    ],
                    "additionalProperties": False
                },

                "sentiment_analysis": {
                    "type": "object",
                    "properties": {
                        "summary": {"type": "string", "description": "Overall market sentiment based on news"},
                        "positive_news": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "headline": {"type": "string"},
                                    "date": {"type": "string"},
                                    "link": {"type": "string"}
                                },
                                "required": ["headline", "date", "link"],
                                "additionalProperties": False
                            }
                        },
                        "negative_news": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "headline": {"type": "string"},
                                    "date": {"type": "string"},
                                    "link": {"type": "string"}
                                },
                                "required": ["headline", "date", "link"],
                                "additionalProperties": False
                            }
                        },
                        "neutral_news": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "headline": {"type": "string"},
                                    "date": {"type": "string"},
                                    "link": {"type": "string"}
                                },
                                "required": ["headline", "date", "link"],
                                "additionalProperties": False
                            }
                        }
                    },
                    "required": ["summary", "positive_news", "negative_news", "neutral_news"],
                    "additionalProperties": False
                },

                "halal_screening": {
                    "type": "object",
                    "properties": {
                        "status": {
                            "type": "string",
                            "enum": ["Halal", "Haram", "Cannot Determine"],
                            "description": "Overall Shariah-compliance classification"
                        },
                        "business_activity_assessment": {
                            "type": "string",
                            "description": "Assessment of whether the company's core business sector is permissible, or a note that sector data was unavailable"
                        },
                        "financial_ratio_assessment": {
                            "type": "string",
                            "description": "Assessment of interest-bearing debt, interest income, and illiquid asset ratios against common screening thresholds, or a note that this data was unavailable"
                        },
                        "reasoning": {
                            "type": "string",
                            "description": "Overall explanation for the status, including any specific missing data points that prevented a definitive Halal/Haram determination"
                        }
                    },
                    "required": [
                        "status", "business_activity_assessment",
                        "financial_ratio_assessment", "reasoning"
                    ],
                    "additionalProperties": False
                },

                "investment_outlook": {
                    "type": "object",
                    "properties": {
                        "verdict": {
                            "type": "string",
                            "description": "e.g. 'Buy x%', 'Sell x%', 'Skip x%'"
                        },
                        "rationale": {"type": "string",
                                      "description": "Clear reasoning combining technical, fundamental, and sentiment data"},
                        "short_term": {"type": "string",
                                       "description": "Short-term trading strategy based on analysis"},
                        "long_term": {"type": "string",
                                      "description": "Long-term investment strategy based on analysis"}
                    },
                    "required": ["verdict", "rationale", "short_term", "long_term"],
                    "additionalProperties": False
                },

                "Suggestions": {
                    "type": "object",
                    "properties": {
                        "entry_points": {"type": "string",
                                         "description": "Suggested entry points based on technical analysis"},
                        "exit_points": {"type": "string",
                                        "description": "Suggested exit points based on technical analysis"},
                        "risk_management": {"type": "string",
                                            "description": "Advice on managing risks based on volatility and sentiment"},
                        "diversification": {"type": "string",
                                            "description": "Suggestions for portfolio diversification if applicable"},
                        "monitoring": {"type": "string",
                                       "description": "Advice on how frequently to monitor this stock"},
                        "missing_data": {"type": "string",
                                         "description": "List of any missing data points that could improve analysis"}
                    },
                    "required": [
                        "entry_points", "exit_points", "risk_management",
                        "diversification", "monitoring", "missing_data"
                    ],
                    "additionalProperties": False
                }
            },
            "required": [
                "stock_name", "Currency", "CurrencySymbol",
                "technical_overview", "fundamental_overview",
                "sentiment_analysis", "halal_screening",
                "investment_outlook", "Suggestions"
            ],
            "additionalProperties": False
        }
    }

    return prompt, output_format


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

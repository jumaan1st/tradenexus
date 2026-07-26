from google import genai
from utils.text import filter_backticks
import config

client = genai.Client(api_key=config.GEMINI_API_KEY)


def generate_content(prompt):
    """Generate content via Gemini, with fallback to older model."""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
    except Exception as e:
        print(f"Error with gemini-2.5-flash: {e}. Falling back to gemini-2.0-flash.")
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
    return filter_backticks(response.text)

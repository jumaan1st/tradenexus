from filter import filter
import os
from google import genai
from google.genai import types

from dotenv import load_dotenv
load_dotenv()

# client = genai.Client(api_key="AIzaSyD3REvTgic6cII3HoxlF5BpIgaxtkfbxl4")
api_key = os.environ.get("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)



def generate_content(prompt):
    try:
        # Attempt to use the primary model (gemini-2.0-flash)

        response = client.models.generate_content(
            model="gemini-2.5-flash", contents=prompt
        )
    except Exception as e:
        print(f"Error with gemini-2.0-flash: {e}. Falling back to gemini-1.5-flash.")
        # If the primary model fails, use the fallback model (gemini-1.5-flash)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
    return filter(response.text)
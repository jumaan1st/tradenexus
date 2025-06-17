from google import genai
from filter import filter

client = genai.Client(api_key="AIzaSyAc8Fm4e8P51IvYNaAjeHMZcAxrPW-j1K8")


def generate_content(prompt):
    try:
        # Attempt to use the primary model (gemini-2.0-flash)
        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=prompt
        )
    except Exception as e:
        print(f"Error with gemini-2.0-flash: {e}. Falling back to gemini-1.5-flash.")
        # If the primary model fails, use the fallback model (gemini-1.5-flash)
        response = client.models.generate_content(
            model="gemini-1.5-flash", contents=prompt
        )
    return filter(response.text)
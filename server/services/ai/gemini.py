from google import genai
from services.ai.base import AIClient
from utils.text import filter_backticks


class GeminiClient(AIClient):
    def __init__(self, api_key, model=None):
        self.client = genai.Client(api_key=api_key)
        self.model = model or "gemini-2.5-flash"
        self.fallback_model = "gemini-2.0-flash"

    def _call(self, contents):
        try:
            response = self.client.models.generate_content(
                model=self.model, contents=contents
            )
        except Exception as e:
            print(f"Error with {self.model}: {e}. Falling back to {self.fallback_model}.")
            response = self.client.models.generate_content(
                model=self.fallback_model, contents=contents
            )
        return filter_backticks(response.text)

    def generate(self, prompt, system=None):
        contents = prompt if not system else f"{system}\n\n{prompt}"
        return self._call(contents)

    def chat(self, messages, system=None):
        parts = []
        if system:
            parts.append(system)
        for msg in messages:
            parts.append(msg.get("content", ""))
        return self._call("\n\n".join(parts))

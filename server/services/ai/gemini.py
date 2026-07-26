from google import genai
from google.genai import types

from services.ai.base import AIClient
from utils.text import filter_backticks


class GeminiClient(AIClient):
    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model

    def _call(self, contents, system=None, output_format=None):
        config_args = {}

        if system:
            config_args["system_instruction"] = system

        if output_format:
            config_args["response_mime_type"] = "application/json"
            config_args["response_schema"] = output_format

        config = types.GenerateContentConfig(**config_args) if config_args else None

        response = self.client.models.generate_content(
            model=self.model,
            contents=contents,
            config=config,
        )

        return filter_backticks(response.text)

    def generate(self, prompt: str, system: str | None = None, output_format: dict | None = None) -> str:
        return self._call(contents=prompt, system=system, output_format=output_format)

    def chat(self, messages: list[dict], system: str | None = None, output_format: dict | None = None) -> str:
        formatted_contents = []

        for message in messages:
            role = "user" if message.get("role") == "user" else "model"
            content = message.get("content", "")

            formatted_contents.append(
                types.Content(
                    role=role,
                    parts=[types.Part.from_text(text=content)]
                )
            )

        return self._call(contents=formatted_contents, system=system, output_format=output_format)
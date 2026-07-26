from openai import OpenAI
from services.ai.base import AIClient
from utils.text import filter_backticks


class DeepSeekClient(AIClient):
    def __init__(self, api_key, base_url=None, model=None):
        self.client = OpenAI(
            api_key=api_key,
            base_url=base_url or "https://api.deepseek.com"
        )
        self.model = model or "deepseek-chat"

    def _call(self, messages):
        response = self.client.chat.completions.create(
            model=self.model,
            messages=messages,
            stream=False
        )
        return filter_backticks(response.choices[0].message.content)

    def generate(self, prompt, system=None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        else:
            messages.append({"role": "system", "content": "You are a helpful finance adviser."})
        messages.append({"role": "user", "content": prompt})
        return self._call(messages)

    def chat(self, messages, system=None):
        formatted = []
        if system:
            formatted.append({"role": "system", "content": system})
        else:
            formatted.append({"role": "system", "content": "You are a helpful finance adviser."})
        for msg in messages:
            if "role" in msg and "content" in msg:
                formatted.append(msg)
            elif "user" in msg:
                formatted.append({"role": "user", "content": msg["user"]})
            elif "bot" in msg:
                formatted.append({"role": "assistant", "content": msg["bot"]})
        return self._call(formatted)

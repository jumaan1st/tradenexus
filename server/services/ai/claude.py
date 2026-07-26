import anthropic
from services.ai.base import AIClient
from utils.text import filter_backticks


class ClaudeClient(AIClient):
    def __init__(self, api_key, model):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model

    def _call(self, messages, system=None):
        kwargs = {"model": self.model, "max_tokens": 4096, "messages": messages}
        if system:
            kwargs["system"] = system
        response = self.client.messages.create(**kwargs)
        return filter_backticks(response.content[0].text)

    def generate(self, prompt, system=None):
        messages = [{"role": "user", "content": prompt}]
        return self._call(messages, system=system)

    def chat(self, messages, system=None):
        formatted = []
        for msg in messages:
            if "role" in msg and "content" in msg:
                formatted.append({"role": msg["role"], "content": msg["content"]})
            elif "user" in msg:
                formatted.append({"role": "user", "content": msg["user"]})
            elif "bot" in msg:
                formatted.append({"role": "assistant", "content": msg["bot"]})
        return self._call(formatted, system=system)

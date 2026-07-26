import ollama
from services.ai.base import AIClient


class OllamaClient(AIClient):
    def __init__(self, model=None):
        self.model = model or "llama3.1"

    def generate(self, prompt, system=None):
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        response = ollama.chat(model=self.model, messages=messages)
        return response['message']['content']

    def chat(self, messages, system=None):
        formatted = []
        if system:
            formatted.append({"role": "system", "content": system})
        for msg in messages:
            if "role" in msg and "content" in msg:
                formatted.append(msg)
            elif "user" in msg:
                formatted.append({"role": "user", "content": msg["user"]})
            elif "bot" in msg:
                formatted.append({"role": "assistant", "content": msg["bot"]})

        response = ollama.chat(model=self.model, messages=formatted)
        return response['message']['content']

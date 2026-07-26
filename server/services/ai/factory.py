import config
from services.ai.base import AIClient

_client = None

DEFAULTS = {
    "gemini": "gemini-2.5-flash",
    "ollama": "llama3.1",
    "deepseek": "deepseek-chat",
}


def get_ai_client() -> AIClient:
    """Return a singleton AI client based on AI_PROVIDER and AI_MODEL env vars.

    Set AI_MODEL in .env to any model name (e.g. gemini-2.0-flash, llama3, deepseek-reasoner).
    If AI_MODEL is empty, uses provider default.
    """
    global _client
    if _client is not None:
        return _client

    provider = config.AI_PROVIDER.lower()
    model = config.AI_MODEL or DEFAULTS.get(provider)

    if provider == "ollama":
        from services.ai.ollama import OllamaClient
        _client = OllamaClient(model=model)

    elif provider == "deepseek":
        from services.ai.deepseek import DeepSeekClient
        _client = DeepSeekClient(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL,
            model=model
        )

    else:
        from services.ai.gemini import GeminiClient
        _client = GeminiClient(api_key=config.GEMINI_API_KEY, model=model)

    return _client

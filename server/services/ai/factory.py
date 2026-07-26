import config
from services.ai.base import AIClient

_client = None


def get_ai_client() -> AIClient:
    """Return a singleton AI client based on AI_PROVIDER env var.

    Providers: gemini (default), ollama, deepseek
    Override model with AI_MODEL env var.
    """
    global _client
    if _client is not None:
        return _client

    provider = config.AI_PROVIDER.lower()

    if provider == "ollama":
        from services.ai.ollama import OllamaClient
        _client = OllamaClient(model=config.AI_MODEL or config.OLLAMA_MODEL)

    elif provider == "deepseek":
        from services.ai.deepseek import DeepSeekClient
        _client = DeepSeekClient(
            api_key=config.DEEPSEEK_API_KEY,
            base_url=config.DEEPSEEK_BASE_URL,
            model=config.AI_MODEL
        )

    else:
        from services.ai.gemini import GeminiClient
        _client = GeminiClient(api_key=config.GEMINI_API_KEY, model=config.AI_MODEL)

    return _client

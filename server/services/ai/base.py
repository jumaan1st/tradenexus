from abc import ABC, abstractmethod


class AIClient(ABC):
    """Unified interface for all AI providers."""

    @abstractmethod
    def generate(self, prompt, system=None):
        """Single prompt → single response. Used for analysis/predictions."""
        ...

    @abstractmethod
    def chat(self, messages, system=None):
        """Conversation (list of role/content dicts) → response. Used for bot."""
        ...

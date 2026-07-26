from abc import ABC, abstractmethod


class AIClient(ABC):
    """Unified interface for all AI providers."""

    @abstractmethod
    def generate(self, prompt, system=None, output_format=None):
        """
        Single prompt → single response.

        Args:
            prompt (str): User prompt.
            system (str, optional): System instruction.
            output_format (dict | None, optional): Provider-specific output format
                (e.g. JSON schema).
        """
        ...

    @abstractmethod
    def chat(self, messages, system=None, output_format=None):
        """
        Conversation (list of role/content dicts) → response.

        Args:
            messages (list): Conversation history.
            system (str, optional): System instruction.
            output_format (dict | None, optional): Provider-specific output format
                (e.g. JSON schema).
        """
        ...


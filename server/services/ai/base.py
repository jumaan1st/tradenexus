import json
import re
from abc import ABC, abstractmethod

JSON_SUFFIX = (
    "\n\nIMPORTANT: Return ONLY valid JSON. No markdown, no backticks, "
    "no explanation — just the raw JSON object."
)


class AIClient(ABC):
    """Unified interface for all AI providers."""

    @abstractmethod
    def generate(self, prompt, system=None):
        """Single prompt → single response (text). Used for analysis/predictions."""
        ...

    @abstractmethod
    def chat(self, messages, system=None):
        """Conversation (list of role/content dicts) → response. Used for bot."""
        ...

    def generate_json(self, prompt, system=None):
        """Single prompt → parsed JSON dict. Appends JSON instruction and parses."""
        raw = self.generate(prompt + JSON_SUFFIX, system=system)
        return _parse_json(raw)


def _parse_json(text):
    """Extract and parse JSON from AI response, handling backticks and extra text."""
    text = text.strip()

    # Try direct parse first
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Extract from markdown code blocks
    match = re.search(r"```(?:json)?\s*\n?(.*?)\n?\s*```", text, re.DOTALL)
    if match:
        try:
            return json.loads(match.group(1).strip())
        except json.JSONDecodeError:
            pass

    # Find first { or [ to last } or ]
    for open_ch, close_ch in [('{', '}'), ('[', ']')]:
        start = text.find(open_ch)
        end = text.rfind(close_ch)
        if start != -1 and end > start:
            try:
                return json.loads(text[start:end + 1])
            except json.JSONDecodeError:
                pass

    raise ValueError(f"Failed to parse JSON from AI response: {text[:200]}")

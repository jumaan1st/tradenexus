import anthropic
from services.ai.base import AIClient
from utils.text import filter_backticks


class ClaudeClient(AIClient):
    def __init__(self, api_key, model, admin_api_key=None):
        self.client = anthropic.Anthropic(api_key=api_key)
        self.model = model
        self.admin_api_key = admin_api_key

    def _call(self, messages, system=None, output_format=None, max_tokens=8192):
        kwargs = {"model": self.model, "max_tokens": max_tokens, "messages": messages}
        if system:
            kwargs["system"] = system
        if output_format:
            schema = output_format.get("schema", output_format)
            kwargs["output_config"] = {
                "format": {
                    "type": "json_schema",
                    "schema": schema,
                }
            }
        response = self.client.messages.create(**kwargs)

        # Don't assume content[0] is the text block -- find it explicitly.
        text = next(
            (block.text for block in response.content if block.type == "text"),
            ""
        )

        if response.stop_reason == "refusal":
            raise RuntimeError(
                "Claude declined to generate this response for safety reasons."
            )

        if response.stop_reason == "max_tokens":
            raise RuntimeError(
                f"Response was truncated at max_tokens={max_tokens} before "
                "completing the JSON structure. Increase max_tokens and retry."
            )

        return text if output_format else filter_backticks(text)

    def generate(self, prompt, system=None, output_format=None):
        messages = [{"role": "user", "content": prompt}]
        return self._call(messages, system=system, output_format=output_format)

    def chat(self, messages, system=None, output_format=None):
        formatted = []
        for msg in messages:
            if "role" in msg and "content" in msg:
                formatted.append({"role": msg["role"], "content": msg["content"]})
            elif "user" in msg:
                formatted.append({"role": "user", "content": msg["user"]})
            elif "bot" in msg:
                formatted.append({"role": "assistant", "content": msg["bot"]})
        return self._call(formatted, system=system, output_format=output_format)

    def credit_balance(self):
        if not self.admin_api_key:
            raise NotImplementedError(
                "Anthropic has no live balance endpoint for standard API keys. "
                "Pass admin_api_key when constructing ClaudeClient to query "
                "recent spend via the Usage and Cost API, or check "
                "console.anthropic.com/settings/billing directly."
            )
        import requests
        from datetime import datetime, timedelta, timezone

        ending_at = datetime.now(timezone.utc)
        starting_at = ending_at - timedelta(days=1)
        resp = requests.get(
            "https://api.anthropic.com/v1/organizations/usage_report/messages",
            headers={
                "x-api-key": self.admin_api_key,
                "anthropic-version": "2023-06-01",
            },
            params={
                "starting_at": starting_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "ending_at": ending_at.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "bucket_width": "1d",
            },
            timeout=10,
        )
        resp.raise_for_status()
        return resp.json()
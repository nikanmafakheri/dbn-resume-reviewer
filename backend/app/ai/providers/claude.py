"""Claude / Anthropic provider."""

import json
import logging

import httpx

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class ClaudeProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY
        self.base_url = "https://api.anthropic.com/v1"
        self.model = "claude-sonnet-4-20250514"

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        if not self.api_key:
            raise RuntimeError("CLAUDE_API_KEY is not configured")

        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }

        try:
            async with httpx.AsyncClient(timeout=120) as client:
                resp = await client.post(
                    f"{self.base_url}/messages",
                    headers={
                        "x-api-key": self.api_key,
                        "anthropic-version": "2023-06-01",
                        "Content-Type": "application/json",
                    },
                    json=kwargs,
                )
                resp.raise_for_status()
                result = resp.json()
                content = result["content"][0]["text"]
        except httpx.HTTPStatusError as exc:
            logger.error("Claude request failed (%s): %.200s", resp.status_code, resp.text)
            raise RuntimeError(f"Claude request failed ({resp.status_code})") from exc
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            logger.exception("Claude request failed")
            raise RuntimeError(f"Claude request failed: {exc}") from exc

        if not content:
            raise RuntimeError("Claude returned an empty response")

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("Claude returned non-JSON response; falling back to raw")
            return {"raw": content}

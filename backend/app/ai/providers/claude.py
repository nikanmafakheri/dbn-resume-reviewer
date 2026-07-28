"""Claude / Anthropic provider."""

import json
import logging
from pydantic import BaseModel

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
        kwargs = {
            "model": self.model,
            "max_tokens": 4096,
            "messages": [{"role": "user", "content": prompt}],
        }

        if schema is not None and issubclass(schema, BaseModel):
            kwargs["metadata"] = {"user_id": "dbn-resume-reviewer"}

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

        try:
            return json.loads(content)
        except (json.JSONDecodeError, KeyError):
            return {"raw": content}

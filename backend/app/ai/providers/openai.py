"""OpenAI / OpenRouter-compatible provider."""

import json
import logging
from pydantic import BaseModel

import httpx
from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4o"

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        messages = [{"role": "user", "content": prompt}]
        kwargs = {"model": self.model, "messages": messages}

        if schema is not None and issubclass(schema, BaseModel):
            kwargs["response_format"] = {"type": "json_object"}

        async with httpx.AsyncClient(timeout=120) as client:
            resp = await client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
                json=kwargs,
            )
            resp.raise_for_status()
            result = resp.json()
            content = result["choices"][0]["message"]["content"]

        try:
            return json.loads(content)
        except (json.JSONDecodeError, KeyError):
            return {"raw": content}

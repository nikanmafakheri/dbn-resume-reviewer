"""OpenAI / OpenRouter-compatible provider."""

import json
import logging

import httpx
from pydantic import BaseModel

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"
        self.model = "gpt-4o"

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        if not self.api_key:
            raise RuntimeError("OPENAI_API_KEY is not configured")

        messages = [{"role": "user", "content": prompt}]
        kwargs = {"model": self.model, "messages": messages}

        if schema is not None and issubclass(schema, BaseModel):
            # json_object mode requires the word "json" to appear in the prompt
            kwargs["response_format"] = {"type": "json_object"}

        try:
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
        except httpx.HTTPStatusError as exc:
            logger.error("OpenAI request failed (%s): %.200s", resp.status_code, resp.text)
            raise RuntimeError(f"OpenAI request failed ({resp.status_code})") from exc
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            logger.exception("OpenAI request failed")
            raise RuntimeError(f"OpenAI request failed: {exc}") from exc

        if not content:
            raise RuntimeError("OpenAI returned an empty response")

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("OpenAI returned non-JSON response; falling back to raw")
            return {"raw": content}

"""InferX provider — the single LLM provider (OpenAI-compatible gateway).

InferX (the user calls it "infraX") serves OpenAI-compatible endpoints for
serverless GPU inference. This is the only provider wired into the app:
``LLM_PROVIDER`` was removed; ``create_scorer``/``get_llm_provider`` always
return this class.

Doc/catalog: https://model.inferx.net/catalog/endpoints/deepseek-v4-flash?tenant=tn-1e5q8va4so
"""

import json
import logging

import httpx
from pydantic import BaseModel

from app.ai.providers.base import (
    BaseLLMProvider,
    ProviderRateLimitError,
    is_rate_limit_error,
)
from app.core.config import settings

logger = logging.getLogger(__name__)


class InferXProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.INFERX_API_KEY
        self.base_url = settings.INFERX_BASE_URL
        self.model = settings.INFERX_MODEL

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        if not self.api_key:
            raise RuntimeError("INFERX_API_KEY is not configured")

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
            logger.error("InferX request failed (%s): %.200s", resp.status_code, resp.text)
            message = f"InferX request failed ({resp.status_code})"
            if resp.status_code == 429 or is_rate_limit_error(exc):
                raise ProviderRateLimitError(message) from exc
            raise RuntimeError(message) from exc
        except (httpx.HTTPError, KeyError, IndexError) as exc:
            logger.exception("InferX request failed")
            raise RuntimeError(f"InferX request failed: {exc}") from exc

        if not content:
            raise RuntimeError("InferX returned an empty response")

        try:
            return json.loads(content)
        except json.JSONDecodeError:
            logger.warning("InferX returned non-JSON response; falling back to raw")
            return {"raw": content}

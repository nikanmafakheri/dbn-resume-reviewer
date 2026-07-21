"""OpenAI / OpenRouter-compatible provider."""

import httpx
from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings


class OpenAIProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.OPENAI_API_KEY
        self.base_url = "https://api.openai.com/v1"

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        # TODO: implement OpenAI chat completions call
        raise NotImplementedError

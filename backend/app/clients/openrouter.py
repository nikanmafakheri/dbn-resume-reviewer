"""OpenRouter / OpenAI HTTP client."""

import httpx
from app.core.config import settings


class OpenRouterClient:
    def __init__(self):
        self.api_key = settings.OPENROUTER_API_KEY or settings.OPENAI_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.client = httpx.AsyncClient(timeout=120)

    async def chat_completion(self, prompt: str) -> dict:
        resp = await self.client.post(
            f"{self.base_url}/chat/completions",
            headers={"Authorization": f"Bearer {self.api_key}"},
            json={"model": "openai/gpt-4o", "messages": [{"role": "user", "content": prompt}]},
        )
        resp.raise_for_status()
        return resp.json()

    async def close(self):
        await self.client.aclose()

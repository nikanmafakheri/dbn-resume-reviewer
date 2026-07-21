"""OpenRouter provider — routes to multiple models."""

from app.ai.providers.openai import OpenAIProvider


class OpenRouterProvider(OpenAIProvider):
    def __init__(self):
        super().__init__()
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"

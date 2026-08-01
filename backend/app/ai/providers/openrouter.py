"""OpenRouter provider — routes to multiple models."""

from app.ai.providers.base import BaseLLMProvider
from app.ai.providers.openai import OpenAIProvider
from app.core.config import settings


class OpenRouterProvider(OpenAIProvider):
    """OpenAI-compatible provider pointed at OpenRouter.

    Does not call the parent constructor: OpenRouter uses its own API key and
    base URL, and the parent would incorrectly demand OPENAI_API_KEY.
    """

    def __init__(self):
        BaseLLMProvider.__init__(self)  # satisfy ABC without reading OPENAI key
        self.api_key = settings.OPENROUTER_API_KEY
        self.base_url = "https://openrouter.ai/api/v1"
        self.model = "openai/gpt-4o"

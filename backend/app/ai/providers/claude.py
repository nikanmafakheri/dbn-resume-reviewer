"""Claude / Anthropic provider."""

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings


class ClaudeProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.CLAUDE_API_KEY

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        # TODO: implement Anthropic API call
        raise NotImplementedError

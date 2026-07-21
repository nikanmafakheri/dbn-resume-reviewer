"""Abstract base for LLM providers."""

from abc import ABC, abstractmethod


class BaseLLMProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        """Send a prompt to the LLM and return the parsed response.

        Args:
            prompt: The full prompt string.
            schema: Optional Pydantic model class for structured output.

        Returns:
            Parsed response as a dictionary.
        """
        ...

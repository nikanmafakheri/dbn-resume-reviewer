"""Gemini (Google AI) provider — free tier via google-generativeai SDK."""

import json
import logging
from pydantic import BaseModel

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = "gemini-1.5-flash"  # free tier

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name)

        generation_config = {}
        if schema is not None and issubclass(schema, BaseModel):
            generation_config["response_mime_type"] = "application/json"
            generation_config["response_schema"] = schema

        response = await model.generate_content_async(
            prompt,
            generation_config=generation_config or None,
        )

        text = response.text.strip()

        # If response is JSON inside markdown fences, extract it
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return {"raw": text}

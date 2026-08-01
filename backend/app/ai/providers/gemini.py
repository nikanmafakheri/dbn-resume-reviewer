"""Gemini (Google AI) provider — free tier via google-generativeai SDK."""

import json
import logging

from app.ai.providers.base import BaseLLMProvider
from app.core.config import settings

logger = logging.getLogger(__name__)


class GeminiProvider(BaseLLMProvider):
    def __init__(self):
        self.api_key = settings.GEMINI_API_KEY
        self.model_name = settings.GEMINI_MODEL

    async def generate(self, prompt: str, schema: type | None = None) -> dict:
        if not self.api_key:
            raise RuntimeError("GEMINI_API_KEY is not configured")

        # NOTE: `google.generativeai` (deprecated) rejects pydantic schemas
        # when it converts them to its own Schema proto ("Unknown field:
        # default"). The scoring prompt already specifies a strict JSON shape,
        # so we only ask for JSON output — parsing/clamping happens in the
        # score parser, which is provider-agnostic.
        import google.generativeai as genai

        genai.configure(api_key=self.api_key)
        model = genai.GenerativeModel(self.model_name)

        generation_config = {"response_mime_type": "application/json"}

        try:
            response = await model.generate_content_async(
                prompt,
                generation_config=generation_config or None,
            )
        except Exception as exc:
            logger.exception("Gemini request failed")
            raise RuntimeError(f"Gemini request failed: {exc}") from exc

        text = (response.text or "").strip()
        if not text:
            raise RuntimeError("Gemini returned an empty response")

        # If response is JSON inside markdown fences, extract it
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

        try:
            return json.loads(text)
        except json.JSONDecodeError:
            logger.warning("Gemini returned non-JSON response; falling back to raw")
            return {"raw": text}

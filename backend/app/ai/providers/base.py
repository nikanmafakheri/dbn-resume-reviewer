"""Abstract base for LLM providers."""

import re
from abc import ABC, abstractmethod

#: Matches the provider error messages that mean "rate limited / quota
#: exhausted / 429" — used to classify a failure as retryable rather than a bug.
RATE_LIMIT_RE = re.compile(
    r"\b(429|quota|rate\s*limit|exceeded|resource\s*exhausted)\b",
    re.IGNORECASE,
)

#: Matches the error messages that mean "request took too long / was cancelled".
TIMEOUT_RE = re.compile(
    r"\b(time\s*out|timed\s*out|timeout|deadline\s*exceeded|cancelled?)\b",
    re.IGNORECASE,
)


def is_rate_limit_error(exc: Exception) -> bool:
    """True if ``exc`` (or its wrapped message) signals quota/rate-limit.

    Providers raise ``RuntimeError`` with the SDK message embedded; this lets
    them classify cheaply by string without importing each SDK's exception
    types.
    """
    return bool(RATE_LIMIT_RE.search(str(exc)))


def is_timeout_error(exc: Exception) -> bool:
    """True if ``exc`` (or its wrapped message) signals a request timeout.

    Used alongside :func:`is_rate_limit_error` to classify a failure as a
    transient capacity pause (``error_code="timed_out"``) rather than a bug.
    """
    return bool(TIMEOUT_RE.search(str(exc)))


class ProviderRateLimitError(RuntimeError):
    """Raised when the LLM provider is rate-limited or out of quota.

    Distinguishes a retryable capacity pause (``error_code="rate_limited"``)
    from a genuine bug, so the frontend can show a friendly "please wait"
    card instead of a red failure.
    """


class ProviderTimeoutError(RuntimeError):
    """Raised when a single LLM request exceeds its time budget.

    Like :class:`ProviderRateLimitError`, this is a transient capacity pause
    (``error_code="timed_out"``), not a bug — the user is invited to wait and
    retry rather than shown a red failure.
    """


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

"""Retries and error typing

D2 Applications & Integration · 33.1% of the exam.

Not every error should be retried. The SDK raises distinct exception types,
and the exam's "recovery strategy selection" skill is about matching the
strategy to the error class:

Error · Retry? — Why
`RateLimitError` (429) · Yes, with backoff — Transient, capacity-driven
`APIConnectionError` · Yes, with backoff — Network blip
`InternalServerError` (5xx) · Yes, with backoff — Server-side transient
`BadRequestError` (400) · **No** — Your payload is wrong; retrying repeats it
`AuthenticationError` (401) · **No** — Bad key; retrying never fixes it

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

import random
import time

import anthropic
from common import MODEL, client

RETRYABLE = (
    anthropic.RateLimitError,
    anthropic.APIConnectionError,
    anthropic.InternalServerError,
)


def call_with_backoff(prompt: str, max_attempts: int = 4) -> str:
    """Call the API, retrying only errors that retrying can actually fix.

    Uses exponential backoff with jitter so concurrent clients do not
    retry in lockstep and re-create the spike that caused the 429.
    """
    for attempt in range(1, max_attempts + 1):
        try:
            response = client.messages.create(
                model=MODEL,
                max_tokens=100,
                messages=[{"role": "user", "content": prompt}],
            )
            return "".join(
                block.text for block in response.content if block.type == "text"
            )

        except RETRYABLE as error:
            if attempt == max_attempts:
                raise
            delay = (2**attempt) + random.uniform(0, 1)
            print(
                f"attempt {attempt} failed ({type(error).__name__}); "
                f"retrying in {delay:.1f}s"
            )
            time.sleep(delay)

        except (anthropic.BadRequestError, anthropic.AuthenticationError):
            # Deterministic failures: fail fast, do not burn retries.
            raise

    raise RuntimeError("unreachable")


if __name__ == "__main__":
    print(call_with_backoff("Say 'retry logic works' and nothing else."))

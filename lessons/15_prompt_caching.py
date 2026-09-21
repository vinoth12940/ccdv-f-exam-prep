"""5.2 Cost and Token Management (2.8%)

D5 Model Selection & Optimization · 16.8% of the exam.

Rates below are from Anthropic's pricing docs as of September 2026. Prices
change — the exam tests the *shape* of the calculation and the relative
ordering of the tiers, not the digits.

Two multipliers matter most:

- **Batch API**: 50% off input and output.
- **Prompt caching**: a cache read costs 0.1x base input. A 5-minute cache
  write costs 1.25x, a 1-hour write costs 2x. So a 5-minute cache pays for
  itself after **one** read; a 1-hour cache after **two**.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
"""

import anthropic
from common import MODEL, client

RATES = {
    "claude-opus-5": {"input": 5.00, "output": 25.00},
    "claude-sonnet-5": {"input": 2.00, "output": 10.00},
    "claude-haiku-4-5-20251001": {"input": 1.00, "output": 5.00},
}


CACHE_READ_MULTIPLIER = 0.1


CACHE_WRITE_5M_MULTIPLIER = 1.25


CACHE_WRITE_1H_MULTIPLIER = 2.0


BATCH_MULTIPLIER = 0.5


def estimate_cost(
    model: str,
    input_tokens: int = 0,
    output_tokens: int = 0,
    cache_read_tokens: int = 0,
    cache_write_tokens: int = 0,
    batch: bool = False,
    cache_ttl: str = "5m",
) -> float:
    """Return the USD cost of a request.

    Cached reads are billed at a fraction of base input; cache writes at a
    premium. The batch discount multiplies the whole total.
    """
    rate = RATES[model]
    write_multiplier = (
        CACHE_WRITE_5M_MULTIPLIER if cache_ttl == "5m" else CACHE_WRITE_1H_MULTIPLIER
    )

    cost = (
        input_tokens * rate["input"]
        + output_tokens * rate["output"]
        + cache_read_tokens * rate["input"] * CACHE_READ_MULTIPLIER
        + cache_write_tokens * rate["input"] * write_multiplier
    ) / 1_000_000

    return cost * BATCH_MULTIPLIER if batch else cost


volume, tokens_in, tokens_out = 10_000, 2_000, 500


def cache_breakeven(model: str, cached_tokens: int, ttl: str) -> None:
    """Show after how many reads a cache write pays for itself."""
    rate = RATES[model]["input"]
    multiplier = CACHE_WRITE_5M_MULTIPLIER if ttl == "5m" else CACHE_WRITE_1H_MULTIPLIER

    uncached_per_call = cached_tokens * rate / 1_000_000
    write_once = cached_tokens * rate * multiplier / 1_000_000
    read_per_call = cached_tokens * rate * CACHE_READ_MULTIPLIER / 1_000_000

    print(f"{model} | {cached_tokens:,} cached tokens | ttl={ttl}")
    print(f"  no cache, per call : ${uncached_per_call:.4f}")
    print(f"  cache write (once) : ${write_once:.4f}")
    print(f"  cache read per call: ${read_per_call:.4f}")

    for calls in range(1, 6):
        without = uncached_per_call * calls
        with_cache = write_once + read_per_call * (calls - 1)
        verdict = "cache wins" if with_cache < without else "cache loses"
        print(f"  {calls} call(s): ${without:.4f} vs ${with_cache:.4f} -> {verdict}")
    print()


POLICY_MANUAL = (
    "SECTION 1. COVERED PERILS. Fire, lightning, windstorm, hail, "
    "explosion, riot, aircraft, vehicles, smoke, vandalism, theft, "
    "falling objects, weight of ice and snow, accidental water discharge. "
) * 120


def ask_with_cache(question: str) -> anthropic.types.Message:
    """Send a question against a cached policy manual prefix.

    cache_control marks the breakpoint: everything up to and including
    this block is cacheable. Variable content must come after it.
    """
    return client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=[
            {
                "type": "text",
                "text": "You answer coverage questions from the manual.",
            },
            {
                "type": "text",
                "text": POLICY_MANUAL,
                "cache_control": {"type": "ephemeral"},
            },
        ],
        messages=[{"role": "user", "content": question}],
    )


def show_cache_usage(label: str, response: anthropic.types.Message) -> None:
    """Print the cache-specific fields of a usage object."""
    usage = response.usage
    print(
        f"{label:12} input={usage.input_tokens:<6} "
        f"cache_write={usage.cache_creation_input_tokens:<6} "
        f"cache_read={usage.cache_read_input_tokens:<6}"
    )


if __name__ == "__main__":
    for model in RATES:
        realtime = volume * estimate_cost(model, tokens_in, tokens_out)
        batched = volume * estimate_cost(model, tokens_in, tokens_out, batch=True)
        print(f"{model:32} realtime ${realtime:8.2f}   batch ${batched:8.2f}")

    cache_breakeven(MODEL, cached_tokens=50_000, ttl="5m")

    cache_breakeven(MODEL, cached_tokens=50_000, ttl="1h")

    show_cache_usage("first call", ask_with_cache("Is hail covered?"))

    show_cache_usage("second call", ask_with_cache("Is flood covered?"))

    show_cache_usage("third call", ask_with_cache("Is theft covered?"))

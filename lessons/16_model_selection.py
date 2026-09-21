"""5.3 Model Selection and Tradeoffs (2.7%)

D5 Model Selection & Optimization · 16.8% of the exam.

The tiers, in plain terms:

- **Haiku** — fastest and cheapest. Classification, extraction, routing,
  high-volume simple work.
- **Sonnet** — the default for most production workloads. Balanced.
- **Opus** — complex agentic work, long multi-step reasoning, hard code.

The exam gives you a scenario with constraints and asks which tier fits.
The trap answer is always "use the biggest model" — a scenario that
specifies high volume and simple work is testing whether you downshift.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
NEW IN THIS LESSON: recommend_model, scenarios, compare_tiers
Everything above it is repeated from an earlier lesson so this
file runs on its own — skip past it.
"""

import anthropic
from common import HAIKU, MODEL, OPUS, SONNET, client, extract_text

# --- repeated from 15_prompt_caching.py so this lesson runs on its own ---
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


def recommend_model(
    complexity: str, latency_critical: bool, volume_per_day: int
) -> str:
    """Recommend a tier from task shape.

    complexity: "simple" | "moderate" | "complex".
    """
    if complexity == "complex":
        return f"{OPUS} (capability dominates; accept cost and latency)"

    if complexity == "simple" and (latency_critical or volume_per_day > 5_000):
        return f"{HAIKU} (simple work at speed/scale; cheapest per call)"

    if latency_critical and complexity == "moderate":
        return (
            f"{HAIKU} (latency budget rules out larger tiers; "
            "verify quality with evals)"
        )

    return f"{SONNET} (balanced default for production workloads)"


scenarios = [
    ("Route 50k support emails to a queue", "simple", True, 50_000),
    ("Draft a nuanced denial letter", "moderate", False, 300),
    ("Multi-step agent refactoring a codebase", "complex", False, 50),
    ("Autocomplete in an IDE", "simple", True, 200_000),
]


def compare_tiers(prompt: str, max_tokens: int = 200) -> None:
    """Run one prompt across all three tiers and report cost and latency.

    This is how you should actually pick a model: measure on YOUR task,
    not on a benchmark someone else ran.
    """
    import time

    for model in (HAIKU, SONNET, OPUS):
        start = time.perf_counter()
        response = client.messages.create(
            model=model,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        elapsed = time.perf_counter() - start
        cost = estimate_cost(
            model,
            response.usage.input_tokens,
            response.usage.output_tokens,
        )
        print(f"{model:32} {elapsed:5.2f}s  ${cost:.6f}")
        print(f"  {extract_text(response).strip()[:110]}\n")


if __name__ == "__main__":
    for label, complexity, latency, volume in scenarios:
        print(f"{label}\n  -> {recommend_model(complexity, latency, volume)}\n")

    compare_tiers("Classify this claim in one word: roof hail damage, covered.")

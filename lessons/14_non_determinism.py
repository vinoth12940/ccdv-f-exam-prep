"""Non-determinism

D5 Model Selection & Optimization · 16.8% of the exam.

The same prompt does not guarantee the same output. This is a property of how
the model samples the next token, and it is the reason you cannot write a test
that asserts exact string equality on model output. Assert on structure and on
properties instead — Domain 4 builds directly on this.

**What changed:** you no longer have a `temperature` dial. Sampling parameters
(`temperature`, `top_p`, `top_k`) were removed from the current models; the SDK
rejects the keyword before a request is even sent. Non-determinism is now
something you design around, not something you tune.

The cell below shows the shape of it, and the shape is more interesting than a
single number: **how much variation you get depends on how constrained the
output is.** An open-ended generation varies on every run. A tightly constrained
classification is stable in practice — but "stable in practice" is not a
contract, and building a test on exact equality is still wrong.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
"""

from common import MODEL, client, extract_text


def sample_repeatedly(label: str, prompt: str, max_tokens: int, runs: int = 4) -> None:
    """Run the same prompt several times and show the spread."""
    outputs = []
    for _ in range(runs):
        response = client.messages.create(
            model=MODEL,
            max_tokens=max_tokens,
            messages=[{"role": "user", "content": prompt}],
        )
        outputs.append(extract_text(response).strip())

    print(f"--- {label} ---")
    for index, text in enumerate(outputs, start=1):
        print(f"  run {index}: {text[:90]}")
    print(f"  distinct outputs: {len(set(outputs))}/{runs}\n")


if __name__ == "__main__":
    sample_repeatedly(
        "open-ended generation",
        "Write a 3-sentence story about an insurance adjuster.",
        max_tokens=200,
    )

    sample_repeatedly(
        "constrained classification",
        "Claim: water damage found during inspection, cause undetermined. "
        "Reply with exactly one word: APPROVE, DENY, or REVIEW.",
        max_tokens=10,
    )

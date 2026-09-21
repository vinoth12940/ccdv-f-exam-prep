"""Extended thinking, and what replaced the token budget

D5 Model Selection & Optimization · 16.8% of the exam.

Extended thinking gives the model a scratchpad before it answers. You buy
accuracy on multi-step reasoning with tokens and latency.

**The mechanics changed, and the blueprint tests the new ones.** The old fixed
budget — `thinking={"type": "enabled", "budget_tokens": N}` — is removed on the
current models and returns a 400. What replaced it:

- **Adaptive thinking**: `thinking={"type": "adaptive"}`. The model decides when
  to think and how much. On Opus 5 it is on by default, so omitting `thinking`
  entirely still runs adaptive.
- **Effort**: `output_config={"effort": "low"|"medium"|"high"|"xhigh"|"max"}`,
  default `high`. This is the lever for trading thoroughness against spend
  *within one model*. It is model-gated — Haiku 4.5 rejects it.
- **Display**: `thinking={"type": "adaptive", "display": "summarized"}` returns a
  readable summary of the reasoning. The default is `"omitted"`, which streams
  thinking blocks with empty text.

One trap worth burning in: **`display` changes visibility only.** Thinking still
happens and is billed identically under every setting. If you want to spend
less, lower `effort` — do not hide the output.

The exam angle is the tradeoff, not the syntax: high effort on a simple
classification is wasted money; low effort on a multi-constraint reasoning
problem costs you correctness.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
"""

import anthropic
from common import MODEL, client, extract_text

PUZZLE = (
    "A claim was filed 45 days after the loss. The policy requires filing "
    "within 30 days, except that a declared state of emergency extends the "
    "deadline by 60 days. The emergency was declared 10 days BEFORE the "
    "loss and lifted 5 days after it. Is the filing timely? Answer yes or "
    "no, then give the deadline date arithmetic."
)


def answer_at_effort(question: str, effort: str) -> anthropic.types.Message:
    """Adaptive thinking at a chosen effort level.

    `effort` is the modern replacement for a fixed thinking-token budget:
    the model decides how much to think, you decide how much that is worth.
    """
    return client.messages.create(
        model=MODEL,
        max_tokens=4000,
        thinking={"type": "adaptive", "display": "summarized"},
        output_config={"effort": effort},
        messages=[{"role": "user", "content": question}],
    )


if __name__ == "__main__":
    for level in ("low", "high"):
        result = answer_at_effort(PUZZLE, level)
        print(f"=== effort={level} ===")
        print("blocks:", [block.type for block in result.content])
        print("output tokens:", result.usage.output_tokens)
        print(extract_text(result)[:400])
        print()

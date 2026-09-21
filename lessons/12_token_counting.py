"""5.1 LLM Fundamentals — counting tokens before you spend them

D5 Model Selection & Optimization · 16.8% of the exam.

The token-counting endpoint tells you the input size of a request **without
running it**. This is how you enforce a budget at the boundary instead of
discovering the cost on the invoice.

Note that tokenisers differ between model generations, so a count is only
valid for the model you asked about.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
"""

from common import HAIKU, MODEL, SONNET, client


def count_input_tokens(model: str, system: str, user_text: str) -> int:
    """Return the input token count for a request, without sending it."""
    result = client.messages.count_tokens(
        model=model,
        system=system,
        messages=[{"role": "user", "content": user_text}],
    )
    return result.input_tokens


system_prompt = "You are a claims triage classifier."


claim = "Hail damage to roof; adjuster estimate $8,400; policy covers hail."


def enforce_token_budget(model: str, system: str, user_text: str, budget: int) -> None:
    """Reject a request that would exceed the input token budget.

    Checking before the call is the point: once you send it you have
    already paid for it.
    """
    tokens = count_input_tokens(model, system, user_text)
    if tokens > budget:
        raise ValueError(f"request needs {tokens} input tokens, budget is {budget}")
    print(f"within budget: {tokens}/{budget} tokens")


if __name__ == "__main__":
    for model in (SONNET, HAIKU):
        tokens = count_input_tokens(model, system_prompt, claim)
        print(f"{model:32} {tokens:>5} input tokens")

    enforce_token_budget(MODEL, system_prompt, claim, budget=100)

    try:
        enforce_token_budget(MODEL, system_prompt, "word " * 500, budget=100)
    except ValueError as error:
        print("rejected:", error)

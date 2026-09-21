"""4.3 Isolating the origin — worked cases

D4 Eval, Testing & Debugging · 2.6% of the exam.

Run the diagnostic below, then reason through each case yourself before
reading the verdict.

Source: notebooks/08_domain4_eval_testing_and_debugging.ipynb
"""


def diagnose(symptom: str, origin: str, fix: str) -> None:
    """Print a structured diagnosis of one failure."""
    print(f"SYMPTOM : {symptom}")
    print(f"ORIGIN  : {origin}")
    print(f"FIX     : {fix}\n")


if __name__ == "__main__":
    diagnose(
        "TypeError: get_claim() got an unexpected keyword argument 'id'",
        "Integration layer",
        "The schema advertises 'id' but the function takes 'claim_id'. The "
        "model did exactly what the schema said. Align the two.",
    )

    diagnose(
        "Model reports APPROVED when the tool_result clearly said DENIED",
        "Model output",
        "Inputs were correct; reasoning was not. Strengthen the prompt, add "
        "a validator that cross-checks the answer against the tool_result, "
        "and consider a stronger tier if it persists.",
    )

    diagnose(
        "400 error: tool_use ids in the assistant turn have no tool_result",
        "Integration layer",
        "Every tool_use block needs a matching tool_result in the very next "
        "user message. You are almost certainly handling only the first of "
        "several parallel calls.",
    )

    diagnose(
        "Retry loop makes three identical calls and fails identically",
        "Integration layer",
        "The retry resends the original prompt without telling the model what "
        "was wrong. Append the validation error to the conversation so the "
        "next attempt has new information.",
    )

    diagnose(
        "Agent runs 40 turns and never finishes",
        "Integration layer (missing guardrail)",
        "No turn limit. Bound the loop, and inspect the trace for the turn "
        "where progress stopped -- usually a tool returning something the "
        "model cannot act on.",
    )

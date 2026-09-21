"""A workflow: fixed, predetermined steps

D1 Agents & Workflows · 14.7% of the exam.

Note what this buys you — each step is independently testable, the cost is
knowable in advance, and there is no loop to run away.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

import json

from common import HAIKU, client, extract_text


def classify(claim_text: str) -> str:
    """Step 1: assign a category."""
    response = client.messages.create(
        model=HAIKU,
        max_tokens=10,
        system="Reply with one word: PROPERTY, AUTO, or LIABILITY.",
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response).strip()


def extract_amount(claim_text: str) -> str:
    """Step 2: pull the monetary figure."""
    response = client.messages.create(
        model=HAIKU,
        max_tokens=20,
        system="Reply with only the dollar amount, or NONE.",
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response).strip()


def summarise(claim_text: str) -> str:
    """Step 3: one-line summary."""
    response = client.messages.create(
        model=HAIKU,
        max_tokens=60,
        system="Summarise the claim in one short sentence.",
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response).strip()


def claim_intake_workflow(claim_text: str) -> dict[str, str]:
    """Run a fixed three-step pipeline. No model decides the sequence."""
    return {
        "category": classify(claim_text),
        "amount": extract_amount(claim_text),
        "summary": summarise(claim_text),
    }


if __name__ == "__main__":
    result = claim_intake_workflow(
        "Claim ABC-123: hail damaged the roof of the insured dwelling. "
        "Adjuster estimates $8,400 in repairs."
    )

    print(json.dumps(result, indent=2))

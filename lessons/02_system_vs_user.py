"""The system parameter is separate from messages

D2 Applications & Integration · 33.1% of the exam.

Instructions about *how Claude should behave* go in `system`. The
conversation goes in `messages`. Putting persistent instructions in a user
message works less reliably and wastes them on every turn — this is the
"system versus user placement" skill that also appears in Domain 6.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

from common import MODEL, client, extract_text


def classify_claim(claim_text: str) -> str:
    """Classify a claim using a system prompt for the persistent role."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=10,
        system=(
            "You are a claims triage classifier. Respond with exactly one "
            "word: APPROVE, DENY, or REVIEW. Never explain your answer."
        ),
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response).strip()


examples = [
    "Kitchen fire destroyed cabinets; policy includes fire coverage.",
    "Claimant reports gradual roof deterioration from normal aging.",
    "Water damage discovered during inspection; cause not yet determined.",
]


if __name__ == "__main__":
    for claim in examples:
        print(f"{classify_claim(claim):8} <- {claim}")

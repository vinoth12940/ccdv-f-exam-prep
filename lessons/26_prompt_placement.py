"""6.1 Prompt Engineering — placement

D6 Prompt & Context Engineering · 11.0% of the exam.

Persistent role and rules go in `system`. The specific task goes in the
user turn. Two reasons: the model weights system content as standing
instruction, and a stable system block is what prompt caching can reuse.

Source: notebooks/04_domain6_prompt_and_context_engineering.ipynb
"""

from common import MODEL, client, extract_text

CLAIM = (
    "Insured reports water damage in the basement. Sump pump failed during "
    "heavy rain. Policy has a sump pump failure endorsement. No prior "
    "claims. Estimate $6,100."
)


def prompt_everything_in_user() -> str:
    """Anti-pattern: rules and task jumbled into one user message."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        messages=[
            {
                "role": "user",
                "content": (
                    "You are a claims adjuster, be concise, reply APPROVE "
                    f"DENY or REVIEW with one reason. {CLAIM}"
                ),
            }
        ],
    )
    return extract_text(response).strip()


def prompt_with_system_split() -> str:
    """Preferred: standing rules in system, task in the user turn."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=150,
        system=(
            "You are a claims adjuster. Reply with a verdict word "
            "(APPROVE, DENY, REVIEW) followed by a colon and one short "
            "reason. Never exceed 25 words."
        ),
        messages=[{"role": "user", "content": CLAIM}],
    )
    return extract_text(response).strip()


if __name__ == "__main__":
    print("mixed into user:\n ", prompt_everything_in_user(), "\n")

    print("system + user:\n ", prompt_with_system_split())

"""Zero-shot, single-shot, multi-shot

D6 Prompt & Context Engineering · 11.0% of the exam.

Examples teach format and edge-case handling more reliably than prose
description does. Where the exam presses: if output format is drifting,
add examples — do not add more adjectives to the instruction.

Source: notebooks/04_domain6_prompt_and_context_engineering.ipynb
"""

from common import MODEL, client, extract_text

AMBIGUOUS = (
    "Insured noticed cracked floor tiles. Unclear whether from settling "
    "(excluded) or a one-time impact (covered). No inspection yet."
)


def zero_shot(claim_text: str) -> str:
    """No examples: the model infers the format from the instruction."""
    response = client.messages.create(
        model=MODEL,
        max_tokens=30,
        system="Classify as APPROVE, DENY, or REVIEW. One word only.",
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response).strip()


def multi_shot(claim_text: str) -> str:
    """Examples pin down both the format and the edge-case policy.

    The third example is deliberately an ambiguous case labelled REVIEW,
    which teaches the behaviour the instruction alone leaves open.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=30,
        system="Classify as APPROVE, DENY, or REVIEW. One word only.",
        messages=[
            {
                "role": "user",
                "content": "Kitchen fire, fire peril covered, $22,000.",
            },
            {"role": "assistant", "content": "APPROVE"},
            {
                "role": "user",
                "content": "Gradual roof wear from age; wear is excluded.",
            },
            {"role": "assistant", "content": "DENY"},
            {
                "role": "user",
                "content": "Damage cause undetermined; no inspection done.",
            },
            {"role": "assistant", "content": "REVIEW"},
            {"role": "user", "content": claim_text},
        ],
    )
    return extract_text(response).strip()


if __name__ == "__main__":
    print("zero-shot :", zero_shot(AMBIGUOUS))

    print("multi-shot:", multi_shot(AMBIGUOUS))

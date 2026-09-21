"""6.3 Output Handling — validate, do not trust

D6 Prompt & Context Engineering · 11.0% of the exam.

Confident prose is not evidence of correctness. Two defences, and the exam
wants both:

1. **Structural** — validate against a schema, repair or reject on failure.
2. **Semantic** — check the claim against your own source of truth. The
   model can be perfectly well-formed and still wrong about the facts.

Source: notebooks/04_domain6_prompt_and_context_engineering.ipynb
"""

import json

from common import MODEL, client, extract_text
from pydantic import BaseModel, Field, ValidationError


class CoverageAnswer(BaseModel):
    """Contract for a coverage determination."""

    covered: bool
    clause: str = Field(min_length=3, max_length=60)
    confidence: float = Field(ge=0.0, le=1.0)


COVERED_PERILS = {"fire", "hail", "windstorm", "theft", "vandalism"}


EXCLUDED_PERILS = {"flood", "earthquake", "wear", "neglect"}


def parse_structured(raw: str) -> CoverageAnswer | None:
    """Structural check. Returns None instead of raising on bad shape."""
    try:
        return CoverageAnswer.model_validate_json(raw)
    except (ValidationError, json.JSONDecodeError) as error:
        print(f"  structural failure: {error}")
        return None


def verify_semantically(peril: str, answer: CoverageAnswer) -> bool:
    """Semantic check against ground truth we control.

    A well-formed answer that contradicts the policy data is still wrong.
    Never let schema validity stand in for factual verification.
    """
    peril = peril.lower()
    if peril in COVERED_PERILS and not answer.covered:
        print(f"  semantic failure: {peril} IS covered but model said no")
        return False
    if peril in EXCLUDED_PERILS and answer.covered:
        print(f"  semantic failure: {peril} is EXCLUDED but model said yes")
        return False
    return True


def check_coverage(peril: str) -> CoverageAnswer | None:
    """Ask, then verify structurally and semantically before trusting.

    `output_config` constrains generation to the schema, so a structural
    failure here should be impossible. `parse_structured` stays anyway --
    partly as defence in depth, and partly because the moment the JSON comes
    from somewhere you did not constrain (a tool result, a file, another
    service) the structural layer is the only thing standing between you and
    a confusing downstream error.

    What structured outputs does NOT buy you is the semantic check below.
    A schema-perfect answer can still contradict the policy data.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system="Standard homeowner policy. Decide whether the peril is covered.",
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "covered": {"type": "boolean"},
                        "clause": {"type": "string"},
                        "confidence": {"type": "number"},
                    },
                    "required": ["covered", "clause", "confidence"],
                    "additionalProperties": False,
                },
            }
        },
        messages=[{"role": "user", "content": f"Is {peril} damage covered?"}],
    )

    print(f"{peril}:")
    answer = parse_structured(extract_text(response))
    if answer is None:
        return None
    if not verify_semantically(peril, answer):
        return None

    print(f"  accepted: {answer.model_dump()}")
    return answer


if __name__ == "__main__":
    for peril in ("hail", "flood", "fire"):
        check_coverage(peril)

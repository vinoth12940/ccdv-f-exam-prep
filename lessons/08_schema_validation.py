"""2.3 Claude Application Design (8.6%)

D2 Applications & Integration · 33.1% of the exam.

Never trust model output structurally. Validate against a schema, and when
validation fails, feed the **error text** back so the model can self-correct
rather than blindly resending the same prompt.

This same pattern is Domain 6's "defensive parsing" and "skepticism toward
confident output" — it shows up under multiple skill headings.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

from common import MODEL, client
from pydantic import BaseModel, Field, ValidationError


class ClaimDecision(BaseModel):
    """Strict contract for what the model is allowed to return."""

    claim_id: str = Field(pattern=r"^[A-Z]{3}-\d{3}$")
    decision: str = Field(pattern=r"^(APPROVE|DENY|REVIEW)$")
    confidence: float = Field(ge=0.0, le=1.0)
    rationale: str = Field(max_length=200)


def decide_claim(claim_text: str, max_attempts: int = 3) -> ClaimDecision:
    """Get a valid decision, repairing in-loop if validation still fails.

    Structured outputs already guarantee the JSON parses and satisfies the
    schema -- including the field patterns and numeric bounds above. So this
    loop is no longer defending against malformed JSON; it defends against
    the failures a schema cannot express, and it is the pattern you reach for
    whenever validation is richer than the schema (cross-field rules,
    lookups against your own data, business invariants).

    The part worth keeping either way: on failure, send the *exact* error
    back. Telling the model what was wrong is what makes a retry useful --
    a bare retry usually reproduces the same mistake.
    """
    system = (
        "You are a claims decision engine. Decide the claim. When evidence "
        "is incomplete, prefer REVIEW over guessing."
    )
    messages: list[dict] = [{"role": "user", "content": claim_text}]

    for attempt in range(1, max_attempts + 1):
        response = client.messages.parse(
            model=MODEL,
            max_tokens=400,
            system=system,
            output_format=ClaimDecision,
            messages=messages,
        )

        try:
            decision = response.parsed_output
            if decision.confidence < 0.5 and decision.decision != "REVIEW":
                raise ValidationError.from_exception_data(
                    "ClaimDecision",
                    [
                        {
                            "type": "value_error",
                            "loc": ("decision",),
                            "input": decision.decision,
                            "ctx": {"error": "confidence below 0.5 must decide REVIEW"},
                        }
                    ],
                )
            return decision
        except ValidationError as error:
            print(f"attempt {attempt}: rejected -> {error}")
            if attempt == max_attempts:
                raise
            messages.append(
                {
                    "role": "user",
                    "content": (
                        f"That answer was rejected:\n{error}\n"
                        "Reconsider and answer again."
                    ),
                }
            )

    raise RuntimeError("unreachable")


if __name__ == "__main__":
    decision = decide_claim(
        "Claim ABC-123: hail damage to roof. Policy covers hail. "
        "Adjuster confirmed $8,400 damage, no exclusions apply."
    )

    print(decision.model_dump_json(indent=2))

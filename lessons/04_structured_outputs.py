"""Forcing a response shape with structured outputs

D2 Applications & Integration · 33.1% of the exam.

Older code seeded the reply by appending an `assistant` message as the last
entry (`{"role": "assistant", "content": "{"}`) so the model could not emit a
preamble. **Assistant prefill was removed** — on Sonnet 5, Opus 5, and the whole
4.6-and-later family it returns a 400.

Structured outputs replaced it, and they are strictly better: instead of
nudging the model toward JSON, the API *constrains* generation so the response
must satisfy your schema.

Two forms:

- `client.messages.parse(..., output_format=YourPydanticModel)` — validates and
  hands you a typed object in `response.parsed_output`.
- `client.messages.create(..., output_config={"format": {"type": "json_schema",
  "schema": {...}}})` — raw JSON Schema, when you do not want a Pydantic
  dependency.

Note the naming: on `create()` it is `output_config={"format": ...}`. A bare
top-level `output_format` on `create()` is the deprecated spelling.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

from common import MODEL, client
from pydantic import BaseModel


class ClaimExtract(BaseModel):
    """The exact shape we require back. This IS the output contract."""

    claim_id: str
    peril: str
    estimated_amount: float


def extract_claim_json(description: str) -> ClaimExtract:
    """Return a validated object -- no parsing, no repair, no prefill."""
    response = client.messages.parse(
        model=MODEL,
        max_tokens=300,
        output_format=ClaimExtract,
        messages=[{"role": "user", "content": description}],
    )
    return response.parsed_output


if __name__ == "__main__":
    parsed = extract_claim_json(
        "Claim ABC-123: hail damage to the roof, adjuster estimates $8,400."
    )

    print(parsed.model_dump_json(indent=2))

    print("type:", type(parsed))

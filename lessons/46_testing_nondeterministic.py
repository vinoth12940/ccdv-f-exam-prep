"""4.2 Testing non-deterministic output

D4 Eval, Testing & Debugging · 2.6% of the exam.

You cannot assert exact string equality on model output — it varies run to
run. Assert on **properties** instead: does it validate against the schema,
is it in the allowed set, does it agree with ground truth?

And run each case several times. A single green run on a stochastic system
tells you almost nothing; a pass rate does.

Source: notebooks/08_domain4_eval_testing_and_debugging.ipynb
"""

from common import MODEL, client, extract_text


def get_verdict(claim_text: str) -> str:
    """Return the raw JSON string the model produced.

    Structured outputs guarantee this parses and matches the schema, which
    removes one whole class of test failure -- so what the eval below
    measures is the *decision*, not the formatting.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "decision": {
                            "type": "string",
                            "enum": ["APPROVE", "DENY", "REVIEW"],
                        },
                        "reason": {"type": "string"},
                    },
                    "required": ["decision", "reason"],
                    "additionalProperties": False,
                },
            }
        },
        messages=[{"role": "user", "content": claim_text}],
    )
    return extract_text(response)

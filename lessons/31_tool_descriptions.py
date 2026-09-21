"""8.1 Tool Implementation — the description is the prompt

D8 Tools & MCPs · 10.6% of the exam.

A tool's `description` is how the model decides whether and when to call
it. Vague descriptions cause wrong-tool selection, and the exam tests this
directly. A good description states:

1. What the tool does.
2. The exact input format, with an example.
3. What it returns.
4. When *not* to call it, and how it differs from similar tools.

Source: notebooks/05_domain8_tools_and_mcps.ipynb
"""

import json

from common import MODEL, client

WEAK_TOOLS = [
    {
        "name": "search_claims",
        "description": "Search claims.",
        "input_schema": {
            "type": "object",
            "properties": {"q": {"type": "string"}},
            "required": ["q"],
        },
    },
    {
        "name": "get_claim",
        "description": "Get a claim.",
        "input_schema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
    },
]


STRONG_TOOLS = [
    {
        "name": "search_claims",
        "description": (
            "Search claims by free-text criteria such as claimant surname, "
            "peril, or date range, and return up to 20 matching claim IDs "
            "with one-line summaries. Use this when you do NOT already "
            "have a claim ID. Do not use it to fetch details of a known "
            "claim -- call get_claim for that."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": (
                        "Free-text criteria, e.g. 'hail claims filed in "
                        "March 2026' or 'claimant Okafor'."
                    ),
                },
                "limit": {
                    "type": "integer",
                    "minimum": 1,
                    "maximum": 20,
                    "description": "Max results to return. Defaults to 5.",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "get_claim",
        "description": (
            "Retrieve the full record for ONE claim by its exact ID: "
            "status, payout amount, peril, and filing date. Claim IDs have "
            "the format ABC-123. Call once per claim ID. Never invent an "
            "ID -- if you do not have one, call search_claims first."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{3}-[0-9]{3}$",
                    "description": "Exact claim ID, e.g. ABC-123.",
                }
            },
            "required": ["claim_id"],
        },
    },
]


CLAIMS = {
    "ABC-123": {"status": "APPROVED", "amount": 8400, "peril": "hail"},
    "XYZ-789": {"status": "DENIED", "amount": 0, "peril": "flood"},
    "DEF-456": {"status": "PENDING", "amount": 15200, "peril": "fire"},
}


def search_claims(query: str, limit: int = 5) -> str:
    """Naive substring search across the claim records."""
    hits = [
        {"claim_id": claim_id, **record}
        for claim_id, record in CLAIMS.items()
        if query.lower() in json.dumps(record).lower()
    ]
    return json.dumps(hits[:limit])


def get_claim(claim_id: str) -> str:
    """Fetch one claim, or an error string if it does not exist."""
    record = CLAIMS.get(claim_id)
    if record is None:
        return f"ERROR: no claim with id {claim_id}"
    return json.dumps(record)


REGISTRY = {"search_claims": search_claims, "get_claim": get_claim}


def which_tool(tools: list[dict], request: str) -> list[str]:
    """Report which tools the model picks for a request.

    Same request, two tool sets -- the only variable is description
    quality.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=500,
        tools=tools,
        messages=[{"role": "user", "content": request}],
    )
    return [
        f"{block.name}({block.input})"
        for block in response.content
        if block.type == "tool_use"
    ]


request = "Find all the hail claims we have on file."


if __name__ == "__main__":
    print("Compare the two descriptions above before running the next cell.")

    print("weak tools  ->", which_tool(WEAK_TOOLS, request))

    print("strong tools->", which_tool(STRONG_TOOLS, request))

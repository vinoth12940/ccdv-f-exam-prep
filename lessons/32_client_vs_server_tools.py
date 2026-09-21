"""Client-side vs. server-side tools

D8 Tools & MCPs · 10.6% of the exam.

- **Client-side** — you define the schema, you execute the function, you
  return a `tool_result`. Every tool in this notebook is client-side.
- **Server-side** — Anthropic executes it (web search, code execution).
  You do not run a loop for it; results come back inside the response, and
  some carry usage-based pricing beyond tokens.

The exam distinction: a client-side tool needs your execution loop; a
server-side tool does not.

Source: notebooks/05_domain8_tools_and_mcps.ipynb
NEW IN THIS LESSON: run_tool_loop
Everything above it is repeated from an earlier lesson so this
file runs on its own — skip past it.
"""

import json

from common import MODEL, client, extract_text

# --- repeated from 31_tool_descriptions.py so this lesson runs on its own ---
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


def run_tool_loop(request: str, max_turns: int = 6) -> str:
    """Bounded client-side tool loop over STRONG_TOOLS."""
    messages: list[dict] = [{"role": "user", "content": request}]

    for turn in range(1, max_turns + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=STRONG_TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return extract_text(response)

        results = []
        for block in response.content:
            if block.type != "tool_use":
                continue
            output = REGISTRY[block.name](**block.input)
            print(f"turn {turn}: {block.name}({block.input})")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": output,
                    "is_error": output.startswith("ERROR:"),
                }
            )
        messages.append({"role": "user", "content": results})

    return f"STOPPED after {max_turns} turns."


if __name__ == "__main__":
    print(run_tool_loop("Find the hail claims, then give me the full record."))

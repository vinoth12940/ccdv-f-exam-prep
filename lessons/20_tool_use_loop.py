"""1.2 Agent Construction — the tool-use loop

D1 Agents & Workflows · 14.7% of the exam.

An agent is a loop. Claude never executes a tool itself: it returns a
`tool_use` block, **your code** runs the function, and you send the output
back as a `tool_result` block in a new user turn. Repeat until
`stop_reason` is no longer `"tool_use"`.

Four things the exam checks in this loop:

1. Append the assistant's **entire** `response.content`, not just text.
2. Every `tool_use` block needs a matching `tool_result` with the same
   `tool_use_id`, in the very next user message.
3. Handle **multiple** `tool_use` blocks in one response (parallel calls).
4. Bound the loop. An unbounded agent loop is the classic production
   failure — and a classic wrong answer.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

import json

from common import MODEL, client, extract_text

CLAIMS_DB = {
    "ABC-123": {"status": "APPROVED", "amount": 8400, "peril": "hail"},
    "XYZ-789": {"status": "DENIED", "amount": 0, "peril": "flood"},
    "DEF-456": {"status": "PENDING", "amount": 15200, "peril": "fire"},
}


TOOLS = [
    {
        "name": "get_claim",
        "description": (
            "Retrieve status, payout amount, and peril for a single claim "
            "by its ID. Claim IDs have the format ABC-123 (three uppercase "
            "letters, hyphen, three digits). Call once per claim ID. Do "
            "not invent claim IDs that the user did not supply."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_id": {
                    "type": "string",
                    "pattern": "^[A-Z]{3}-[0-9]{3}$",
                    "description": "The claim identifier, e.g. ABC-123.",
                }
            },
            "required": ["claim_id"],
        },
    }
]


def get_claim(claim_id: str) -> str:
    """Look up a claim. Returns an error string rather than raising."""
    record = CLAIMS_DB.get(claim_id)
    if record is None:
        return f"ERROR: no claim found with id {claim_id}"
    return json.dumps(record)


TOOL_REGISTRY = {"get_claim": get_claim}


def run_agent(goal: str, max_turns: int = 6, verbose: bool = True) -> str:
    """Run a bounded tool-use loop and return the final text.

    max_turns is a hard stop. Without it, a model that keeps choosing
    tool_use will loop until your budget or your patience runs out.
    """
    messages: list[dict] = [{"role": "user", "content": goal}]

    for turn in range(1, max_turns + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )

        # Append the FULL content list, including tool_use blocks.
        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [block for block in response.content if block.type == "tool_use"]
        if verbose:
            names = [call.name for call in tool_calls]
            print(f"turn {turn}: stop_reason={response.stop_reason} tools={names}")

        if response.stop_reason != "tool_use":
            return extract_text(response)

        # One tool_result per tool_use, all in a single user message.
        results = []
        for call in tool_calls:
            output = TOOL_REGISTRY[call.name](**call.input)
            if verbose:
                print(f"         {call.name}({call.input}) -> {output}")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": output,
                }
            )
        messages.append({"role": "user", "content": results})

    return f"STOPPED: hit the {max_turns}-turn limit before completing."


if __name__ == "__main__":
    print(run_agent("What is the status of claim ABC-123?"))

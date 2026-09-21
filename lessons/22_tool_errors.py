"""Tool errors belong in tool_result, not in an exception

D1 Agents & Workflows · 14.7% of the exam.

When a tool fails, do not let the exception escape the loop. Send the error
back as a `tool_result` with `is_error: True` and let the model adapt — ask
the user for a correction, try a different argument, or report the failure
cleanly. This is the "feed structured errors back to the model" pattern.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
NEW IN THIS LESSON: run_agent_with_error_handling
Everything above it is repeated from an earlier lesson so this
file runs on its own — skip past it.
"""

import json

from common import MODEL, client, extract_text

# --- repeated from 20_tool_use_loop.py so this lesson runs on its own ---
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


def run_agent_with_error_handling(goal: str, max_turns: int = 6) -> str:
    """Tool-use loop that converts tool exceptions into tool_result errors."""
    messages: list[dict] = [{"role": "user", "content": goal}]

    for turn in range(1, max_turns + 1):
        response = client.messages.create(
            model=MODEL,
            max_tokens=1024,
            tools=TOOLS,
            messages=messages,
        )
        messages.append({"role": "assistant", "content": response.content})

        if response.stop_reason != "tool_use":
            return extract_text(response)

        results = []
        for call in response.content:
            if call.type != "tool_use":
                continue
            try:
                output = TOOL_REGISTRY[call.name](**call.input)
                is_error = output.startswith("ERROR:")
            except (KeyError, TypeError) as error:
                output = f"ERROR: {type(error).__name__}: {error}"
                is_error = True

            print(f"turn {turn}: {call.name}({call.input}) -> {output}")
            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": output,
                    "is_error": is_error,
                }
            )
        messages.append({"role": "user", "content": results})

    return f"STOPPED: hit the {max_turns}-turn limit."


if __name__ == "__main__":
    print(run_agent_with_error_handling("Look up claim QQQ-999 for me."))

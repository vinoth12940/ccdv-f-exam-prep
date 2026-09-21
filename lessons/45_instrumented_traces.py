"""4.1 Instrumented traces

D4 Eval, Testing & Debugging · 2.6% of the exam.

You cannot debug what you cannot see. Record every turn: stop reason, tool
calls, token usage, and errors. This trace is also what produces the
latency and cost numbers you need for Domain 5.

Source: notebooks/08_domain4_eval_testing_and_debugging.ipynb
"""

import json
import time
from dataclasses import dataclass, field

from common import MODEL, client, extract_text


@dataclass
class TurnTrace:
    """One turn of an agent loop."""

    turn: int
    stop_reason: str
    tool_calls: list[str]
    input_tokens: int
    output_tokens: int
    elapsed_seconds: float
    errors: list[str] = field(default_factory=list)


@dataclass
class RunTrace:
    """A whole agent run, with roll-up totals."""

    goal: str
    turns: list[TurnTrace] = field(default_factory=list)
    outcome: str = "incomplete"

    def total_tokens(self) -> tuple[int, int]:
        """Return (input, output) totals across all turns."""
        return (
            sum(turn.input_tokens for turn in self.turns),
            sum(turn.output_tokens for turn in self.turns),
        )

    def report(self) -> None:
        """Print the trace in a form you can actually read."""
        print(f"GOAL    : {self.goal}")
        print(f"OUTCOME : {self.outcome}")
        for turn in self.turns:
            errors = f"  ERRORS={turn.errors}" if turn.errors else ""
            print(
                f"  turn {turn.turn}: stop={turn.stop_reason:<10} "
                f"tools={turn.tool_calls} "
                f"tok={turn.input_tokens}/{turn.output_tokens} "
                f"{turn.elapsed_seconds:.2f}s{errors}"
            )
        tokens_in, tokens_out = self.total_tokens()
        print(
            f"  TOTAL: {tokens_in} in / {tokens_out} out across {len(self.turns)} turns"
        )


CLAIMS = {"ABC-123": {"status": "APPROVED", "amount": 8400}}


TOOLS = [
    {
        "name": "get_claim",
        "description": (
            "Retrieve a claim record by its exact ID (format ABC-123). "
            "Returns status and payout amount."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_id": {"type": "string", "pattern": "^[A-Z]{3}-[0-9]{3}$"}
            },
            "required": ["claim_id"],
        },
    }
]


def get_claim(claim_id: str) -> str:
    """Return a claim record, or an explicit error string."""
    record = CLAIMS.get(claim_id)
    if record is None:
        return f"ERROR: no claim with id {claim_id}"
    return json.dumps(record)


def run_traced_agent(goal: str, max_turns: int = 5) -> RunTrace:
    """Run a bounded agent loop, recording a trace of every turn."""
    trace = RunTrace(goal=goal)
    messages: list[dict] = [{"role": "user", "content": goal}]

    for turn_number in range(1, max_turns + 1):
        start = time.perf_counter()
        response = client.messages.create(
            model=MODEL, max_tokens=1024, tools=TOOLS, messages=messages
        )
        elapsed = time.perf_counter() - start
        messages.append({"role": "assistant", "content": response.content})

        tool_calls = [block for block in response.content if block.type == "tool_use"]
        turn = TurnTrace(
            turn=turn_number,
            stop_reason=response.stop_reason,
            tool_calls=[call.name for call in tool_calls],
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens,
            elapsed_seconds=elapsed,
        )

        if response.stop_reason != "tool_use":
            trace.turns.append(turn)
            trace.outcome = extract_text(response)[:120]
            return trace

        results = []
        for call in tool_calls:
            try:
                output = get_claim(**call.input)
                if output.startswith("ERROR:"):
                    turn.errors.append(output)
            except TypeError as error:
                # Schema and signature disagree: an INTEGRATION bug.
                output = f"ERROR: bad arguments: {error}"
                turn.errors.append(output)

            results.append(
                {
                    "type": "tool_result",
                    "tool_use_id": call.id,
                    "content": output,
                    "is_error": output.startswith("ERROR:"),
                }
            )

        trace.turns.append(turn)
        messages.append({"role": "user", "content": results})

    trace.outcome = f"STOPPED: hit the {max_turns}-turn limit"
    return trace


if __name__ == "__main__":
    run_traced_agent("What is the status of claim ABC-123?").report()

    print()

    run_traced_agent("What is the status of claim QQQ-999?").report()

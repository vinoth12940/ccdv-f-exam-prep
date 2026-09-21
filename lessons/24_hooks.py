"""1.4 Hooks: deterministic control over a non-deterministic system

D1 Agents & Workflows · 14.7% of the exam.

A hook intercepts a tool call **before** it executes and can block it. This
is code, not persuasion — which is precisely why it works where a system
prompt does not. A prompt-level rule can be talked around by injected text;
an `if` statement cannot.

The pattern generalises to human-in-the-loop: block the call, surface it
for approval, execute only on a real approval.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

from dataclasses import dataclass


@dataclass
class HookDecision:
    """Result of a pre-tool-use check."""

    allowed: bool
    reason: str
    needs_human_approval: bool = False


AUTO_APPROVE_LIMIT = 1_000


BLOCKED_TOOLS = {"delete_claim"}


def pre_tool_use_hook(tool_name: str, tool_input: dict) -> HookDecision:
    """Decide whether a tool call may proceed.

    Three outcomes: allow, require human approval, or hard block. Deny by
    policy sits in code so no prompt can argue its way past it.
    """
    if tool_name in BLOCKED_TOOLS:
        return HookDecision(False, f"{tool_name} is disabled in this app")

    if tool_name == "issue_payment":
        amount = tool_input.get("amount", 0)
        if amount > AUTO_APPROVE_LIMIT:
            return HookDecision(
                False,
                f"${amount:,} exceeds the ${AUTO_APPROVE_LIMIT:,} auto-approval limit",
                needs_human_approval=True,
            )

    return HookDecision(True, "within policy")


def issue_payment(claim_id: str, amount: float) -> str:
    """The actual side-effecting operation."""
    return f"PAID ${amount:,.2f} on {claim_id}"


def guarded_call(tool_name: str, tool_input: dict) -> str:
    """Route every tool call through the hook before executing it."""
    decision = pre_tool_use_hook(tool_name, tool_input)

    if decision.allowed:
        return issue_payment(**tool_input)
    if decision.needs_human_approval:
        return f"HELD FOR APPROVAL: {decision.reason}"
    return f"BLOCKED: {decision.reason}"


if __name__ == "__main__":
    print(guarded_call("issue_payment", {"claim_id": "ABC-123", "amount": 500}))

    print(guarded_call("issue_payment", {"claim_id": "DEF-456", "amount": 15200}))

    print(guarded_call("delete_claim", {"claim_id": "XYZ-789"}))

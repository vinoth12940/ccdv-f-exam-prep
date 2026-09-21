"""The injected call meets the policy

D7 Security & Safety · 8.1% of the exam.

Note what happens below: the model was fooled, and it still did not matter.
That is the whole argument for enforcing guardrails in code.

Source: notebooks/06_domain7_security_and_safety.ipynb
NEW IN THIS LESSON: execute_tool_call, injected
Everything above it is repeated from an earlier lesson so this
file runs on its own — skip past it.
"""

from dataclasses import dataclass, field

# --- repeated from 37_defence_not_sufficient.py so this lesson runs on its own ---


@dataclass
class ToolPolicy:
    """Least-privilege policy for one deployment.

    Enumerating what is allowed -- rather than what is forbidden --
    means a newly added tool is denied by default.
    """

    allowed_tools: set[str]
    auto_approve_limit: float = 1_000.0
    audit_log: list[str] = field(default_factory=list)

    def check(self, tool_name: str, tool_input: dict) -> tuple[bool, str]:
        """Return (allowed, reason) and record the decision."""
        if tool_name not in self.allowed_tools:
            decision = (False, f"{tool_name} not granted to this deployment")
        elif tool_name == "issue_payment":
            amount = float(tool_input.get("amount", 0))
            if amount > self.auto_approve_limit:
                decision = (
                    False,
                    (
                        f"${amount:,.2f} exceeds the "
                        f"${self.auto_approve_limit:,.2f} limit; "
                        "needs a human"
                    ),
                )
            else:
                decision = (True, "within auto-approval limit")
        else:
            decision = (True, "permitted")

        self.audit_log.append(
            f"{tool_name} {tool_input} -> "
            f"{'ALLOW' if decision[0] else 'DENY'}: {decision[1]}"
        )
        return decision


JUNIOR_POLICY = ToolPolicy(
    allowed_tools={"get_claim", "search_claims"},
    auto_approve_limit=0.0,
)


SENIOR_POLICY = ToolPolicy(
    allowed_tools={"get_claim", "search_claims", "issue_payment"},
    auto_approve_limit=2_500.0,
)


attempts = [
    ("get_claim", {"claim_id": "ABC-123"}),
    ("issue_payment", {"claim_id": "ATK-001", "amount": 50_000}),
    ("issue_payment", {"claim_id": "ABC-123", "amount": 800}),
]


def execute_tool_call(tool_name: str, tool_input: dict, policy: ToolPolicy) -> str:
    """Execute a tool only if policy allows it.

    Every tool call in a production system goes through a gate like this,
    regardless of how convincing the model's reasoning for it was.
    """
    allowed, reason = policy.check(tool_name, tool_input)
    if not allowed:
        return f"BLOCKED ({reason})"
    return f"EXECUTED {tool_name}({tool_input})"


injected = ("issue_payment", {"claim_id": "ATK-001", "amount": 50_000})


if __name__ == "__main__":
    print("model was persuaded to call:", injected)

    print("result:", execute_tool_call(*injected, SENIOR_POLICY))

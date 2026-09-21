"""Prompt-level defence is necessary but not sufficient

D7 Security & Safety · 8.1% of the exam.

Layer it. The prompt reduces the chance the model is fooled; the hook makes
it not matter if it is. **Defence in depth** is the phrase the exam uses,
and it means assuming the earlier layer will eventually fail.

Source: notebooks/06_domain7_security_and_safety.ipynb
"""

from dataclasses import dataclass, field


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


if __name__ == "__main__":
    for label, policy in (("junior", JUNIOR_POLICY), ("senior", SENIOR_POLICY)):
        print(f"--- {label} ---")
        for tool_name, tool_input in attempts:
            allowed, reason = policy.check(tool_name, tool_input)
            print(f"  {'ALLOW' if allowed else 'DENY ':5} {tool_name}: {reason}")
        print()

    print("audit trail (senior):")

    for entry in SENIOR_POLICY.audit_log:
        print(" ", entry)

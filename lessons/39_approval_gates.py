"""7.2 Human-in-the-loop approval gates

D7 Security & Safety · 8.1% of the exam.

For irreversible or high-impact actions, blocking is not enough — you need
a path for a human to approve. The rule: the gate is the default for write
operations, and the agent never holds the authority to bypass it.

Source: notebooks/06_domain7_security_and_safety.ipynb
NEW IN THIS LESSON: Approval, request_approval, human_decides, gated_call
Everything above it is repeated from an earlier lesson so this
file runs on its own — skip past it.
"""

from dataclasses import dataclass, field
from enum import Enum

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


class Approval(Enum):
    """Outcome of an approval request."""

    APPROVED = "approved"
    REJECTED = "rejected"
    PENDING = "pending"


PENDING_QUEUE: list[dict] = []


def request_approval(tool_name: str, tool_input: dict, reason: str) -> dict:
    """Queue an action for human review instead of executing it."""
    item = {
        "id": f"REQ-{len(PENDING_QUEUE) + 1:03d}",
        "tool": tool_name,
        "input": tool_input,
        "reason": reason,
        "status": Approval.PENDING,
    }
    PENDING_QUEUE.append(item)
    return item


def human_decides(request_id: str, approved: bool) -> str:
    """Apply a human decision. Only this path can execute a gated call."""
    for item in PENDING_QUEUE:
        if item["id"] != request_id:
            continue
        item["status"] = Approval.APPROVED if approved else Approval.REJECTED
        if approved:
            return f"EXECUTED {item['tool']}({item['input']})"
        return f"REJECTED {item['id']}"
    return f"no such request: {request_id}"


def gated_call(tool_name: str, tool_input: dict, policy: ToolPolicy) -> str:
    """Execute, or queue for approval if policy withholds authority."""
    allowed, reason = policy.check(tool_name, tool_input)
    if allowed:
        return f"EXECUTED {tool_name}({tool_input})"

    item = request_approval(tool_name, tool_input, reason)
    return f"QUEUED {item['id']} for human review ({reason})"


if __name__ == "__main__":
    print(
        gated_call(
            "issue_payment", {"claim_id": "DEF-456", "amount": 15_200}, SENIOR_POLICY
        )
    )

    print(human_decides("REQ-001", approved=False))

    print("queue:", [(i["id"], i["status"].value) for i in PENDING_QUEUE])

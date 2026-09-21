"""1.3 Agent Patterns — supervisor and subagents

D1 Agents & Workflows · 14.7% of the exam.

A supervisor decomposes a task and dispatches subtasks to subagents. The
payoff is **context isolation**: each subagent gets a clean, narrow context
containing only what its subtask needs, instead of inheriting the whole
conversation.

Why that matters: a long shared context invites drift, costs more on every
turn, and lets irrelevant earlier content bias later answers. Isolation is
the architectural fix, and it is the reason the exam pairs "subagents" with
"context management" rather than with "speed".

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

import json

from common import MODEL, client, extract_text


def plan_subtasks(task: str, count: int = 3) -> list[str]:
    """Supervisor step: decompose a task into independent subtasks.

    Structured outputs guarantee the shape. Note the schema root is an
    object, not an array -- so the list is wrapped in a `subtasks` key.
    """
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        system=f"Break the task into exactly {count} independent subtasks.",
        output_config={
            "format": {
                "type": "json_schema",
                "schema": {
                    "type": "object",
                    "properties": {
                        "subtasks": {
                            "type": "array",
                            "items": {"type": "string"},
                        }
                    },
                    "required": ["subtasks"],
                    "additionalProperties": False,
                },
            }
        },
        messages=[{"role": "user", "content": task}],
    )
    return json.loads(extract_text(response))["subtasks"]

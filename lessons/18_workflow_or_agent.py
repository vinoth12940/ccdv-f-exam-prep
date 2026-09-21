"""1.1 Workflow or agent?

D1 Agents & Workflows · 14.7% of the exam.

Skill — Weight
Agent Construction with Claude — 5.3%
Agent Patterns and Frameworks — 4.9%
Agent Architecture — 4.5%

A **workflow** runs steps you decided in advance. A **agent** decides its
own steps at runtime. The decision rule:

- Steps known upfront, same every time → workflow. Cheaper, testable,
  debuggable, no runaway risk.
- Number and order of steps depends on what is discovered mid-task → agent.

The exam's trap is reaching for an agent when a workflow would do. Agents
cost more, fail in more ways, and are harder to test. Default to a workflow
and escalate only when the task genuinely needs runtime decisions.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

import os

import anthropic

OPUS = "claude-opus-5"


SONNET = "claude-sonnet-5"


HAIKU = "claude-haiku-4-5-20251001"


MODEL = SONNET


def extract_text(response: anthropic.types.Message) -> str:
    """Concatenate text blocks, ignoring thinking and tool_use blocks."""
    return "".join(block.text for block in response.content if block.type == "text")


if __name__ == "__main__":
    """Shared setup. Export ANTHROPIC_API_KEY before launching Jupyter."""

    client = anthropic.Anthropic()

    print("API key loaded:", bool(os.environ.get("ANTHROPIC_API_KEY")))

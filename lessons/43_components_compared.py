"""3.3 The components, distinguished

D3 Claude Code · 3.1% of the exam.

These five get confused with each other, which is exactly why they are
tested:

Component · What it is · Invoked by — Lives in
**Rules** (CLAUDE.md) · Standing context and conventions, always loaded ·
Nothing — always on
    `CLAUDE.md`
**Skill** · Procedural knowledge, loaded on relevance · Claude, when relevant
    `.claude/skills/`
**Command** · A prompt template you trigger explicitly · You, via `/name`
    `.claude/commands/`
**Subagent** · A separate agent with its own context window · Claude, by
delegation
    `.claude/agents/`
**Agent Memory** · State persisted across sessions · Read and written by the
agent
    Memory store

The distinction the exam presses: a **Command** is user-invoked, a **Skill**
is model-invoked. And a **Subagent** exists for context isolation — a fresh
window, not just a different prompt.

Source: notebooks/07_domain3_claude_code.ipynb
"""

import os

COMMAND = """\
---
description: Review a claims module for schema-validation gaps
---

Review $ARGUMENTS for these specific issues:

1. Any `client.messages.create` result used without schema validation.
2. Any floating model alias in production code (must be a dated ID).
3. Any tool call that writes or pays without passing through
   `guardrails/policy.py`.
4. Any PII reaching a prompt without redaction.

Report findings as a numbered list with file:line references. Do not fix
anything yet.
"""


if __name__ == "__main__":
    os.makedirs(".claude/commands", exist_ok=True)

    with open(".claude/commands/review-claims.md", "w") as handle:
        handle.write(COMMAND)

    print("Invoke with:  /review-claims src/triage.py")

    print()

    print(COMMAND)

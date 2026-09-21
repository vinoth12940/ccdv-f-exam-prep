"""3.1 The CLAUDE.md hierarchy

D3 Claude Code · 3.1% of the exam.

One skill: Claude Code Operation. This domain is configuration and
operational knowledge rather than API code — but it is still worth writing
the files out and reading them, because the exam asks about precedence and
about which component does what.

CLAUDE.md files layer from broad to specific, with more specific scopes
taking precedence:

1. **Enterprise** — org-wide policy, managed centrally.
2. **Project** — committed to the repo, shared with the team. This is
   where the conventions a codebase depends on belong.
3. **Project-local** — your personal overrides for one repo, gitignored.
4. **User** — `~/.claude/CLAUDE.md`, your preferences everywhere.

Rule of thumb: if a teammate checking out the repo would need it, it goes
in the project file and gets committed.

Source: notebooks/07_domain3_claude_code.ipynb
"""

import os

PROJECT_CLAUDE_MD = """\
# Claims Platform

## Stack
Python 3.11, FastAPI, Postgres. Anthropic SDK for all model calls.

## Model policy
- Pinned: `claude-haiku-4-5-20251001` for triage, `claude-sonnet-5` for
  letter drafting.
- Never use a floating alias in `src/production/`. Pin dated IDs so a
  model release cannot silently change behaviour.
- Upgrading a pin requires the eval suite in `evals/` to pass first.

## Conventions
- Type hints on every public function; `ruff` and `mypy` must pass.
- All I/O is async. Use `asyncio.gather` for independent calls.
- Model output is always validated against a pydantic model before use.
  Never trust a raw response body.

## Security
- Never put credentials or PII in prompt content. Redact before the call.
- Tool calls that write or pay go through `guardrails/policy.py`.
- No secrets in this file, in tests, or in fixtures.

## Where things live
- Skills:   `.claude/skills/`
- Commands: `.claude/commands/`
- Subagents:`.claude/agents/`
- Settings: `.claude/settings.json` (shared), `settings.local.json` (yours)
"""


if __name__ == "__main__":
    os.makedirs(".claude", exist_ok=True)

    with open("CLAUDE.md", "w") as handle:
        handle.write(PROJECT_CLAUDE_MD)

    print(PROJECT_CLAUDE_MD)

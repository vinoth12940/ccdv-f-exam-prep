"""3.2 settings.json

D3 Claude Code · 3.1% of the exam.

`settings.json` is committed and shared; `settings.local.json` is personal
and gitignored. The categories it governs are what the exam asks about:
permissions, hooks, environment, and model selection.

Permissions are the important one. `allow` auto-runs, `ask` prompts, and
`deny` blocks outright — and a deny rule is what keeps a destructive
command from ever being one accidental keystroke away.

Source: notebooks/07_domain3_claude_code.ipynb
"""

import json
import os

SETTINGS = {
    "model": "claude-sonnet-5",
    "permissions": {
        "allow": [
            "Read(src/**)",
            "Bash(pytest:*)",
            "Bash(ruff:*)",
        ],
        "ask": [
            "Write(src/**)",
            "Bash(git push:*)",
        ],
        "deny": [
            "Read(.env)",
            "Read(**/secrets/**)",
            "Bash(rm -rf:*)",
            "Bash(curl:*)",
        ],
    },
    "hooks": {
        "PreToolUse": [
            {
                "matcher": "Bash",
                "hooks": [
                    {
                        "type": "command",
                        "command": ".claude/hooks/check_command.sh",
                    }
                ],
            }
        ],
        "PostToolUse": [
            {
                "matcher": "Write|Edit",
                "hooks": [{"type": "command", "command": "ruff check --fix"}],
            }
        ],
    },
    "env": {"CLAIMS_API_BASE": "https://internal.example.com"},
}


HOOK_SCRIPT = """\
#!/usr/bin/env bash
# PreToolUse hook: receives the tool call as JSON on stdin.
# Exit 0 to allow, exit 2 to BLOCK and return stderr to the model.
set -euo pipefail

payload=$(cat)
command=$(echo "$payload" | jq -r '.tool_input.command // ""')

for forbidden in "rm -rf /" "DROP TABLE" "git push --force"; do
  if [[ "$command" == *"$forbidden"* ]]; then
    echo "BLOCKED: '$forbidden' is not permitted in this repo" >&2
    exit 2
  fi
done

exit 0
"""


if __name__ == "__main__":
    with open(".claude/settings.json", "w") as handle:
        json.dump(SETTINGS, handle, indent=2)

    print(json.dumps(SETTINGS, indent=2))

    os.makedirs(".claude/hooks", exist_ok=True)

    with open(".claude/hooks/check_command.sh", "w") as handle:
        handle.write(HOOK_SCRIPT)

    os.chmod(".claude/hooks/check_command.sh", 0o755)

    print(HOOK_SCRIPT)

    print(
        "Exit code 2 is the one that matters: it blocks and tells the model "
        "why, so it can adapt instead of retrying blindly."
    )

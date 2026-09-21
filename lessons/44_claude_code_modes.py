"""3.4 Modes

D3 Claude Code · 3.1% of the exam.

- **Interactive** — the normal REPL session.
- **Headless** (`claude -p "prompt"`) — non-interactive, one shot, exits
  with a status code. This is the CI/CD answer: a pipeline has no terminal
  to type into, so a code-review or migration step runs headless and gates
  the build on its exit code.
- **Streaming** — emits output incrementally, for piping into another
  process or rendering live.
- **Auto-mode** — reduced approval prompting. Powerful and risky: pair it
  with tight `deny` permissions and hooks, because you have removed the
  human who was previously catching mistakes.

Session management matters for cost as much as correctness: a long session
carries its whole history into every turn. Start a fresh session when you
switch tasks rather than letting unrelated context accumulate.

Source: notebooks/07_domain3_claude_code.ipynb
"""

# CCDV-F Exam Prep

Hands-on study material for the **Claude Certified Developer – Foundations**
(CCDV-F) exam. Complete, runnable Python notebooks organised by the official
exam blueprint, weighted so your time goes where the points are.

Not affiliated with or endorsed by Anthropic. Contains no exam content — all
material is written against the publicly published exam guide blueprint.

## Contents

| File | Domain | Blueprint weight |
|---|---|---|
| [`00_STUDY_GUIDE.md`](00_STUDY_GUIDE.md) | **Read first** — every domain in bullets, with self-checks | — |
| [`02_CHEAT_SHEET.md`](02_CHEAT_SHEET.md) | One page to skim on exam morning | — |
| [`notebooks/01_domain2_applications_and_integration.ipynb`](notebooks/01_domain2_applications_and_integration.ipynb) | Applications and Integration | 33.1% |
| [`notebooks/02_domain5_model_selection_and_optimization.ipynb`](notebooks/02_domain5_model_selection_and_optimization.ipynb) | Model Selection and Optimization | 16.8% |
| [`notebooks/03_domain1_agents_and_workflows.ipynb`](notebooks/03_domain1_agents_and_workflows.ipynb) | Agents and Workflows | 14.7% |
| [`notebooks/04_domain6_prompt_and_context_engineering.ipynb`](notebooks/04_domain6_prompt_and_context_engineering.ipynb) | Prompt and Context Engineering | 11.0% |
| [`notebooks/05_domain8_tools_and_mcps.ipynb`](notebooks/05_domain8_tools_and_mcps.ipynb) | Tools and MCPs | 10.6% |
| [`notebooks/06_domain7_security_and_safety.ipynb`](notebooks/06_domain7_security_and_safety.ipynb) | Security and Safety | 8.1% |
| [`notebooks/07_domain3_claude_code.ipynb`](notebooks/07_domain3_claude_code.ipynb) | Claude Code | 3.1% |
| [`notebooks/08_domain4_eval_testing_and_debugging.ipynb`](notebooks/08_domain4_eval_testing_and_debugging.ipynb) | Eval, Testing, and Debugging | 2.6% |

Notebooks `01`–`03` cover roughly 65% of the exam by weight.

## Prefer plain Python? Use [`lessons/`](lessons/)

The same material as 47 small, self-contained `.py` files — one concept each,
numbered in exam-weight order. Average 84 lines. No Jupyter needed.

```bash
cd lessons
export ANTHROPIC_API_KEY=sk-ant-...
python3 01_response_blocks.py
```

Each file opens with a docstring explaining the concept and its exam trap, then
the code, then an `if __name__ == "__main__":` demo. [`lessons/README.md`](lessons/README.md)
is the index and study order. `lessons/common.py` holds the client, the model
IDs and `extract_text()`.

**Pick one source of truth.** `lessons/` was derived from the notebooks and is
maintained separately — edits on one side do not flow to the other.

## What makes this different

- **No fill-in-the-blanks.** Every cell runs as written. Read the concept, run
  it, then change something and run it again.
- **One running domain.** An insurance-claims scenario carries through all eight
  notebooks, so you're not re-reading a new setup every cell.
- **Skimmable.** `00_STUDY_GUIDE.md` is bullets and tables — what each blueprint
  domain tests, the traps, and self-check questions per domain.
- **Lint clean.** All code passes `ruff check` at 88 columns, with type hints
  and docstrings throughout.

## Setup

```bash
git clone https://github.com/<your-username>/ccdv-f-exam-prep.git
cd ccdv-f-exam-prep
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export ANTHROPIC_API_KEY=sk-ant-...      # never commit this
jupyter lab      # or open the folder in VS Code
```

Get an API key from the [Claude Console](https://platform.claude.com/).

## Cost

Running every notebook once costs well under a dollar on Sonnet. The prompt-
caching exercise in notebook `02` sends a ~50k-token prefix three times — the
most expensive cell in the set. Don't loop it.

## Notes before you run

- Notebook `05` writes a working MCP server to disk. Run it from a terminal,
  not a notebook cell — MCP servers own their own process.
- Notebook `07` writes `CLAUDE.md`, `.claude/settings.json`, and a hook script
  into the working directory. Run it somewhere scratch if you don't want those
  landing in a real repo.

## On the numbers

Model IDs and pricing were verified against Anthropic's
[pricing docs](https://platform.claude.com/docs/en/about-claude/pricing) in
September 2026. Prices change — re-check before relying on the figures. The
exam tests the shape of the calculation and the relative ordering of tiers, not
the digits.

## Verifying code style

`lessons/` is lint-clean under the config in [`ruff.toml`](ruff.toml)
(pycodestyle, pyflakes, isort, pyupgrade, bugbear, simplify at 88 columns):

```bash
pip install ruff
ruff check lessons/          # passes
ruff check lessons/ --fix    # after you edit a lesson
```

The notebooks are checked separately, since they are JSON:

```bash
pip install ruff nbconvert
jupyter nbconvert --to script notebooks/*.ipynb
ruff check --line-length 88 notebooks/*.py
rm notebooks/*.py
```

## License

MIT — see [LICENSE](LICENSE).

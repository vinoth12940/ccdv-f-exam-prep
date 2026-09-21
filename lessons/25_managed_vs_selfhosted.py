"""1.5 Managed vs. self-hosted agents

D1 Agents & Workflows · 14.7% of the exam.

- **Self-hosted** — you run the loop, as in every cell above. Full control
  over execution, state, and infrastructure; you also own scaling, session
  persistence, retries, and observability.
- **Anthropic-hosted (Managed Agents)** — Anthropic runs the session.
  Billed on tokens plus session runtime. Less infrastructure work, less
  control over the execution environment.

The selection criteria are the usual build-versus-buy ones: how much you
need to customise the loop, whether your data may leave your environment,
and whether you want to own session state.

Source: notebooks/03_domain1_agents_and_workflows.ipynb
"""

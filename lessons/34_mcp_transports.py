"""Transports

D8 Tools & MCPs · 10.6% of the exam.

- **stdio** — the host launches the server as a subprocess and talks over
  stdin/stdout. Local, single-user, no network surface. The default for
  developer tooling.
- **Streamable HTTP** — the server runs as a network service, serving many
  clients. Needed for remote or shared deployments, and it brings auth and
  network security into scope.

Pick stdio for a local dev tool; pick HTTP when the server must be shared.

Source: notebooks/05_domain8_tools_and_mcps.ipynb
"""

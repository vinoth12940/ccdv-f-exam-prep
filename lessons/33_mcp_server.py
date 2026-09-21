"""8.2 MCP — host, client, server

D8 Tools & MCPs · 10.6% of the exam.

The three roles, precisely — and conflating them is a known exam trap:

- **Host** — the application the user interacts with (Claude Code, Claude
  Desktop, your own app). It owns the conversation and decides when tools
  run.
- **Client** — lives inside the host. One client maintains one connection
  to one server, handling the protocol.
- **Server** — exposes capabilities. It is *called*, never the caller.

The thing people get backwards: your application code that calls the Claude
API is the **host**, not a server. The server is a separate process you
connect to.

An MCP server exposes three kinds of capability:

- **Tools** — model-invoked actions.
- **Resources** — readable context, addressed by URI.
- **Prompts** — reusable templates the user invokes.

Run the next cell to write a working server, then run it in a terminal.

Source: notebooks/05_domain8_tools_and_mcps.ipynb
"""

SERVER_SOURCE = '''"""Minimal MCP server exposing claims capabilities.

Run with:  python claims_mcp_server.py
Install with:  pip install mcp
"""

import json

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("claims-server")

CLAIMS = {
    "ABC-123": {"status": "APPROVED", "amount": 8400, "peril": "hail"},
    "XYZ-789": {"status": "DENIED", "amount": 0, "peril": "flood"},
}


@mcp.tool()
def get_claim(claim_id: str) -> str:
    """Retrieve a claim record by its exact ID (format ABC-123).

    The docstring becomes the tool description the model reads, so it
    carries the same weight as a hand-written description field.
    """
    record = CLAIMS.get(claim_id)
    if record is None:
        return f"ERROR: no claim with id {claim_id}"
    return json.dumps(record)


@mcp.resource("claims://policy-manual")
def policy_manual() -> str:
    """Readable context, addressed by URI. Not model-invoked."""
    return "SECTION 1. COVERED PERILS: fire, hail, windstorm, theft."


@mcp.prompt()
def triage_prompt(claim_text: str) -> str:
    """A reusable template the user invokes, not the model."""
    return f"Triage this claim as APPROVE, DENY or REVIEW:\\n{claim_text}"


if __name__ == "__main__":
    # stdio: the host launches this as a subprocess and speaks over
    # stdin/stdout. Best for local, single-user servers.
    # Streamable HTTP is the alternative for remote, multi-client servers.
    mcp.run(transport="stdio")
'''


if __name__ == "__main__":
    with open("claims_mcp_server.py", "w") as handle:
        handle.write(SERVER_SOURCE)

    print("wrote claims_mcp_server.py")

    print("run it:  pip install mcp && python claims_mcp_server.py")

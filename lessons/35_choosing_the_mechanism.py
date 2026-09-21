"""8.3 Agentic Customization — choosing the mechanism

D8 Tools & MCPs · 10.6% of the exam.

Four ways to extend Claude. The exam gives a scenario and asks which fits:

Mechanism · Use when — Runs where
**Built-in tool** · Anthropic already provides it (web search, code execution)
    Anthropic's infrastructure
**Custom tool** · One app needs one capability; no reuse elsewhere
    Your app's loop
**Skill** · Reusable *instructions and procedure*, not an API call
    Loaded into context
**MCP server** · A capability several apps need, maintained independently
    Its own process

The two decision hinges:

- **Reuse across applications** → MCP server. A custom tool duplicated in
  five codebases is five places to fix a bug.
- **Knowledge versus action** → a Skill teaches Claude *how your team does
  something*; a tool gives it the ability to *do* something external.

Worked answers:

1. *Web search for a research agent* → **built-in tool**. Already exists;
   building your own is wasted work.
2. *One-off CSV reformatting for a single project* → **custom tool** (or a
   Skill if it is procedure rather than code). No reuse, so no MCP.
3. *Inventory lookups needed by five apps, owned by a platform team* →
   **MCP server**. This is the textbook case: shared, independently
   maintained, one place to fix.
4. *"How we write release notes" style guide across many repos* →
   **Skill**. It is procedural knowledge, not an external call.

Source: notebooks/05_domain8_tools_and_mcps.ipynb
"""

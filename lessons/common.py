"""Shared setup for every lesson file.

Each lesson imports what it needs from here, so no lesson has to repeat
the client construction or the model IDs.

    export ANTHROPIC_API_KEY=sk-ant-...

Importing this module never calls the API — the client only talks to
Anthropic when a lesson actually sends a request.
"""

from __future__ import annotations

import os

import anthropic

client = anthropic.Anthropic()

# Current self-serve model IDs (verified against Anthropic docs, Sept 2026).
OPUS = "claude-opus-5"
SONNET = "claude-sonnet-5"
HAIKU = "claude-haiku-4-5-20251001"

# Lessons default to the cheapest model. Point this at SONNET or OPUS when a
# lesson is about capability rather than mechanics.
MODEL = HAIKU


def extract_text(response: anthropic.types.Message) -> str:
    """Return the concatenated text of a response, ignoring other blocks.

    Use this everywhere instead of `response.content[0].text` — a response
    is a *list of typed blocks*, and index 0 is not always a text block.
    This is lesson 01, and it matters in every lesson after it.
    """
    return "".join(block.text for block in response.content if block.type == "text")


def has_api_key() -> bool:
    """True when ANTHROPIC_API_KEY is set, so a lesson can warn instead of crash."""
    return bool(os.environ.get("ANTHROPIC_API_KEY"))


if __name__ == "__main__":
    print("API key loaded:", has_api_key())
    print("Default model :", MODEL)

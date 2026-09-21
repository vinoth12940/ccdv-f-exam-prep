"""2.4 Configuration Management (4.1%)

D2 Applications & Integration · 33.1% of the exam.

`claude-sonnet-5` is an alias that moves as new versions ship. A dated ID
like `claude-haiku-4-5-20251001` is frozen. In production you pin, then
upgrade deliberately after running your evals — otherwise a model release
silently changes your output format and your parser breaks on a Tuesday.

This is the "breaking behavior changes across model releases" point in
Domain 5, enforced through config in Domain 2.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

import json
from dataclasses import asdict, dataclass

from common import client


@dataclass(frozen=True)
class ClaudeConfig:
    """Versioned, serialisable app configuration.

    Everything that changes model behaviour lives here so a change is a
    reviewable diff, not an untracked edit in someone's shell.

    Note what is NOT here any more: `temperature`. Sampling parameters were
    removed from the current models -- the SDK rejects the keyword outright.
    Depth and spend are steered with `output_config={"effort": ...}` instead,
    which is model-gated (Haiku 4.5 does not accept it), so it belongs in the
    per-model config of an app that uses it rather than in this shared shape.
    """

    model: str
    max_tokens: int
    system_prompt_version: str

    def as_request_kwargs(self) -> dict:
        """Return the subset that goes straight into messages.create()."""
        return {
            "model": self.model,
            "max_tokens": self.max_tokens,
        }


PRODUCTION = ClaudeConfig(
    model="claude-haiku-4-5-20251001",  # pinned: dated ID, never an alias
    max_tokens=1024,
    system_prompt_version="triage-v3",
)


DEVELOPMENT = ClaudeConfig(
    model="claude-sonnet-5",  # alias is fine in dev
    max_tokens=1024,
    system_prompt_version="triage-v3",
)


SYSTEM_PROMPTS = {
    "triage-v2": (
        "You are a claims triage classifier. Respond APPROVE, DENY, or REVIEW."
    ),
    "triage-v3": (
        "You are a claims triage classifier. Respond with exactly one "
        "word: APPROVE, DENY, or REVIEW. Never explain. When evidence is "
        "incomplete, prefer REVIEW over guessing."
    ),
}


def run_with_config(config: ClaudeConfig, claim_text: str) -> str:
    """Execute a call using a pinned config and a versioned prompt.

    Prompt text is versioned alongside the model so an eval result can be
    attributed to an exact (model, prompt) pair.
    """
    response = client.messages.create(
        system=SYSTEM_PROMPTS[config.system_prompt_version],
        messages=[{"role": "user", "content": claim_text}],
        **config.as_request_kwargs(),
    )
    return "".join(
        block.text for block in response.content if block.type == "text"
    ).strip()


claim = "Water stain on ceiling; source undetermined; no inspection yet."


if __name__ == "__main__":
    print(json.dumps(asdict(PRODUCTION), indent=2))

    print("\nrequest kwargs:", PRODUCTION.as_request_kwargs())

    for version in ("triage-v2", "triage-v3"):
        config = ClaudeConfig("claude-haiku-4-5-20251001", 10, version)
        print(f"{version}: {run_with_config(config, claim)}")

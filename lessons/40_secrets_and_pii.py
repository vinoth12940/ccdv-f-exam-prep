"""7.3 Secrets and PII

D7 Security & Safety · 8.1% of the exam.

Two rules that carry most of the weight:

1. **A secret never enters a prompt.** Context gets logged, cached, traced,
   and echoed. Keys live in environment variables or a secret manager, read
   by your code, used in the `x-api-key` header — never in message content.
2. **Redact PII before the call**, keeping a local map so you can restore
   it afterwards. The model works on placeholders; the sensitive values
   never leave your process.

Source: notebooks/06_domain7_security_and_safety.ipynb
"""

import os
import re

from common import MODEL, client, extract_text

PII_PATTERNS = {
    "SSN": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "EMAIL": re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.]+\b"),
    "PHONE": re.compile(r"\b\d{3}-\d{3}-\d{4}\b"),
    "CARD": re.compile(r"\b\d{4}[ -]?\d{4}[ -]?\d{4}[ -]?\d{4}\b"),
}


def redact(text: str) -> tuple[str, dict[str, str]]:
    """Replace PII with placeholders and return the restoration map."""
    mapping: dict[str, str] = {}
    redacted = text

    for label, pattern in PII_PATTERNS.items():
        for index, match in enumerate(pattern.findall(redacted), start=1):
            token = f"[{label}_{index}]"
            mapping[token] = match
            redacted = redacted.replace(match, token)

    return redacted, mapping


def restore(text: str, mapping: dict[str, str]) -> str:
    """Put the real values back after the model has done its work."""
    for token, value in mapping.items():
        text = text.replace(token, value)
    return text


original = (
    "Claimant Jane Okafor, SSN 123-45-6789, reachable at jane@example.com "
    "or 555-123-4567. Card on file 4111 1111 1111 1111."
)


def check_secret_hygiene() -> None:
    """Verify a key is present without ever printing its value."""
    key = os.environ.get("ANTHROPIC_API_KEY")

    if not key:
        print("no key found in the environment")
        return

    print("key present : True")
    print(f"length      : {len(key)}")
    print(f"fingerprint : {key[:7]}...{key[-4:]}")
    print("full value  : never printed, never logged, never in a prompt")


def scan_prompt_for_secrets(prompt: str) -> list[str]:
    """Catch credentials before they are sent.

    Run this at the boundary. A leaked key in context is a leaked key in
    every log, cache and trace that context touches.
    """
    patterns = {
        "anthropic key": re.compile(r"sk-ant-[\w-]{10,}"),
        "aws key": re.compile(r"AKIA[0-9A-Z]{16}"),
        "bearer token": re.compile(r"[Bb]earer\s+[\w.-]{20,}"),
        "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    }
    return [label for label, pattern in patterns.items() if pattern.search(prompt)]


dangerous = "Debug this call, my key is sk-ant-api03-ABCDEF123456789"


if __name__ == "__main__":
    redacted, mapping = redact(original)

    print("sent to the model:\n ", redacted)

    response = client.messages.create(
        model=MODEL,
        max_tokens=200,
        system="Rewrite the claim note professionally. Keep placeholders as-is.",
        messages=[{"role": "user", "content": redacted}],
    )

    model_output = extract_text(response)

    print("\nmodel output:\n ", model_output)

    print("\nrestored locally:\n ", restore(model_output, mapping))

    check_secret_hygiene()

    print("\nfindings:", scan_prompt_for_secrets(dangerous))

"""5.4 Technical Fundamentals (6.1%)

D5 Model Selection & Optimization · 16.8% of the exam.

The SDK is a thin convenience layer over a plain REST endpoint. Seeing the
raw call once means you will not be confused by an exam item that describes
HTTP-level behaviour — headers, status codes, the JSON body shape.

Source: notebooks/02_domain5_model_selection_and_optimization.ipynb
"""

import json
import os

import requests
from common import MODEL

API_URL = "https://api.anthropic.com/v1/messages"


def raw_rest_call(prompt: str) -> dict:
    """Call the Messages API over plain HTTP, no SDK.

    Three headers are mandatory: the API key, the API version, and the
    content type. The response JSON has the same shape the SDK parses
    into objects.
    """
    response = requests.post(
        API_URL,
        headers={
            "x-api-key": os.environ["ANTHROPIC_API_KEY"],
            "anthropic-version": "2023-06-01",
            "content-type": "application/json",
        },
        json={
            "model": MODEL,
            "max_tokens": 100,
            "messages": [{"role": "user", "content": prompt}],
        },
        timeout=30,
    )
    response.raise_for_status()
    return response.json()


if __name__ == "__main__":
    payload = raw_rest_call("Reply with exactly: raw REST works.")

    print(json.dumps(payload, indent=2)[:700])

    print("\nSame shape the SDK wraps: content is a list of typed blocks.")

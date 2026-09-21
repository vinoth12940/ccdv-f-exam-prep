"""Streaming

D2 Applications & Integration · 33.1% of the exam.

Streaming delivers incremental events so a UI can render tokens as they
arrive. It **does not reduce cost** — you pay the same per token. Use it
for perceived latency in interactive interfaces.

Exam trap: "we need to reduce cost on a chat feature" → streaming is not
the answer; caching or a smaller model is.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

import anthropic
from common import MODEL, client


def stream_answer(question: str) -> anthropic.types.Message:
    """Stream a response to stdout and return the final assembled Message."""
    with client.messages.stream(
        model=MODEL,
        max_tokens=300,
        messages=[{"role": "user", "content": question}],
    ) as stream:
        for chunk in stream.text_stream:
            print(chunk, end="", flush=True)
        final = stream.get_final_message()

    print("\n---")
    print(f"stop_reason={final.stop_reason} usage={final.usage}")
    return final


if __name__ == "__main__":
    _ = stream_answer("Explain prompt caching in three sentences.")

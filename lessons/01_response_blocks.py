"""2.1 Claude API Mechanics — the response object

D2 Applications & Integration · 33.1% of the exam.

The most important idea to remember:
    response.content is a list of typed blocks, not a single string.

A block can be one of these types:
    - "text"
    - "tool_use"
    - "thinking"

This means code like:
    response.content[0].text

is unsafe because the first block might be a thinking block or a tool call.
The correct approach is to read content by block type, not by index.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

import anthropic
from common import MODEL, client


def describe_response(response: anthropic.types.Message) -> None:
    """Print the structure of a Claude Messages API response.

    This shows why we must filter by block type instead of assuming the
    first item in response.content is always a text block.
    """
    print(f"id          : {response.id}")
    print(f"model       : {response.model}")
    print(f"stop_reason : {response.stop_reason}")
    print(f"blocks      : {[block.type for block in response.content]}")
    print(
        f"usage       : in={response.usage.input_tokens} "
        f"out={response.usage.output_tokens}"
    )

    for block in response.content:
        if block.type == "text":
            print(f"\ntext block  : {block.text}")
        elif block.type == "tool_use":
            print(f"\ntool_use    : {block.name}({block.input})")
        elif block.type == "thinking":
            print(f"\nthinking    : {block.thinking[:120]}...")


def extract_text(response: anthropic.types.Message) -> str:
    """Return only the text blocks from a response.

    This is the safe pattern to use instead of:
        response.content[0].text
    """
    text_parts = []

    for block in response.content:
        if block.type == "text":
            text_parts.append(block.text)

    return "".join(text_parts)


if __name__ == "__main__":
    response = client.messages.create(
        model=MODEL,
        max_tokens=300,
        messages=[
            {
                "role": "user",
                "content": "In two sentences, what is a tool_use content block?",
            }
        ],
    )

    describe_response(response)
    print("\nextract_text() ->", extract_text(response))

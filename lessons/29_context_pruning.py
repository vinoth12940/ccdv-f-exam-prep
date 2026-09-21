"""6.2 Context Engineering — pruning and compaction

D6 Prompt & Context Engineering · 11.0% of the exam.

Context grows every turn. Tool results are usually the worst offender:
verbose, and stale the moment they have been used. Two techniques:

- **Pruning** — replace old tool output with a short placeholder.
- **Compaction** — summarise old turns into a compact note and drop the
  originals.

Both fight "context drift": the degradation that comes from a window
crowded with stale, irrelevant content.

Source: notebooks/04_domain6_prompt_and_context_engineering.ipynb
"""

import copy
import json

from common import HAIKU, client, extract_text


def prune_tool_results(messages: list[dict], keep_recent: int = 1) -> list[dict]:
    """Replace all but the most recent tool_result payloads.

    Returns a new list; the caller's history is untouched. Placeholders
    keep the tool_use/tool_result pairing valid while shedding the bulk.
    """
    pruned = copy.deepcopy(messages)

    indices = [
        index
        for index, message in enumerate(pruned)
        if isinstance(message.get("content"), list)
        and any(
            isinstance(block, dict) and block.get("type") == "tool_result"
            for block in message["content"]
        )
    ]

    for index in indices[:-keep_recent] if keep_recent else indices:
        for block in pruned[index]["content"]:
            if isinstance(block, dict) and block.get("type") == "tool_result":
                block["content"] = "[pruned: superseded tool output]"

    return pruned


def measure(messages: list[dict]) -> int:
    """Rough size proxy: characters of serialised history."""
    return len(json.dumps(messages, default=str))


history = [
    {"role": "user", "content": "Look up ABC-123"},
    {"role": "assistant", "content": "checking"},
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "t1", "content": "A" * 4000}
        ],
    },
    {"role": "user", "content": "Now look up XYZ-789"},
    {"role": "assistant", "content": "checking"},
    {
        "role": "user",
        "content": [
            {"type": "tool_result", "tool_use_id": "t2", "content": "B" * 4000}
        ],
    },
]


def compact_history(messages: list[dict], keep_recent: int = 2) -> list[dict]:
    """Summarise older turns into one note, keeping recent turns verbatim.

    This is what "compaction" means in practice: trade fidelity on old
    turns for room in the window, while the live part of the conversation
    stays exact.
    """
    if len(messages) <= keep_recent:
        return messages

    older, recent = messages[:-keep_recent], messages[-keep_recent:]
    transcript = "\n".join(
        f"{message['role']}: {str(message['content'])[:400]}" for message in older
    )

    response = client.messages.create(
        model=HAIKU,
        max_tokens=250,
        system=(
            "Summarise this conversation history into under 100 words. "
            "Preserve decisions, identifiers, and open questions. Drop "
            "pleasantries and superseded detail."
        ),
        messages=[{"role": "user", "content": transcript}],
    )
    summary = extract_text(response).strip()

    return [
        {"role": "user", "content": f"[earlier conversation]\n{summary}"},
        {"role": "assistant", "content": "Understood, continuing."},
        *recent,
    ]


conversation = [
    {"role": "user", "content": "I want to file a claim for roof damage."},
    {"role": "assistant", "content": "I can help. When did it occur?"},
    {"role": "user", "content": "March 3rd, during the hailstorm."},
    {"role": "assistant", "content": "Noted. Do you have photographs?"},
    {"role": "user", "content": "Yes, twelve photos from the adjuster."},
    {"role": "assistant", "content": "Good. Policy number?"},
    {"role": "user", "content": "POL-88231. What is my deductible?"},
]


if __name__ == "__main__":
    print(f"before pruning: {measure(history):,} chars")

    print(f"after pruning : {measure(prune_tool_results(history)):,} chars")

    for message in compact_history(conversation):
        print(f"{message['role']:10} {str(message['content'])[:150]}")

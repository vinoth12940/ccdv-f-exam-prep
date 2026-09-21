"""Realtime vs. Batch

D2 Applications & Integration · 33.1% of the exam.

The Batch API processes large asynchronous workloads within a 24-hour
window at **50% off both input and output tokens**. The decision rule the
exam tests is purely about latency tolerance:

- Does a human wait on this response? → realtime (Messages API)
- Can it land within 24 hours? → Batch, every time, for half the cost

Note what does *not* change the answer: lowering `max_tokens` or downsizing
the model addresses a different axis entirely.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

from common import MODEL, client


def choose_api(latency_tolerant: bool, request_count: int) -> str:
    """Return the API that fits the workload.

    Batch wins whenever nobody is waiting on the result and there is
    enough volume to be worth the async round trip.
    """
    if latency_tolerant and request_count > 1:
        return "batch (50% cheaper, results within 24h)"
    return "realtime Messages API"


scenarios = [
    ("Overnight analytics over 10,000 documents", True, 10_000),
    ("Live customer support chat turn", False, 1),
    ("Nightly re-scoring of yesterday's claims", True, 4_000),
    ("Interactive IDE autocomplete", False, 1),
]


def submit_batch(prompts: list[str]) -> str:
    """Submit prompts as a batch job and return the batch id.

    Each request needs a custom_id so you can match results back to
    inputs -- results do not come back in submission order.
    """
    requests = [
        {
            "custom_id": f"claim-{index}",
            "params": {
                "model": MODEL,
                "max_tokens": 100,
                "messages": [{"role": "user", "content": prompt}],
            },
        }
        for index, prompt in enumerate(prompts)
    ]

    batch = client.messages.batches.create(requests=requests)
    print(f"batch id       : {batch.id}")
    print(f"status         : {batch.processing_status}")
    print(f"request counts : {batch.request_counts}")
    return batch.id


def collect_batch_results(batch_id: str) -> dict[str, str]:
    """Poll a batch until it ends, then return {custom_id: text}.

    In production you would poll on a schedule or use a webhook rather
    than blocking. Results stream back as JSONL, one entry per request.
    """
    import time

    while True:
        batch = client.messages.batches.retrieve(batch_id)
        print(f"status: {batch.processing_status}")
        if batch.processing_status == "ended":
            break
        time.sleep(10)

    results: dict[str, str] = {}
    for entry in client.messages.batches.results(batch_id):
        if entry.result.type == "succeeded":
            message = entry.result.message
            text = "".join(
                block.text for block in message.content if block.type == "text"
            )
            results[entry.custom_id] = text
        else:
            results[entry.custom_id] = f"FAILED: {entry.result.type}"
    return results


if __name__ == "__main__":
    for label, tolerant, count in scenarios:
        print(f"{label:45} -> {choose_api(tolerant, count)}")

    batch_id = submit_batch(
        [
            "Summarise in one line: hail damage claim, $8,400.",
            "Summarise in one line: kitchen fire claim, $22,000.",
        ]
    )

    for custom_id, text in collect_batch_results(batch_id).items():
        print(f"{custom_id}: {text}")

"""2.2 Software Engineering Foundations (7.4%)

D2 Applications & Integration · 33.1% of the exam.

Independent requests should run concurrently. Running them sequentially
wastes wall-clock time equal to the sum of the latencies rather than the
max. The exam tests that you recognise `asyncio.gather` as the fix.

Source: notebooks/01_domain2_applications_and_integration.ipynb
"""

import asyncio
import concurrent.futures
import time

from anthropic import AsyncAnthropic
from common import MODEL

async_client = AsyncAnthropic()


async def ask_async(question: str) -> str:
    """Send one question and return its text."""
    response = await async_client.messages.create(
        model=MODEL,
        max_tokens=80,
        messages=[{"role": "user", "content": question}],
    )
    return "".join(block.text for block in response.content if block.type == "text")


async def compare_sequential_and_concurrent() -> None:
    """Time the same three independent calls both ways."""
    questions = [
        "Name one peril covered by a standard homeowner policy.",
        "Name one peril usually excluded from a standard policy.",
        "Define 'deductible' in one short sentence.",
    ]

    start = time.perf_counter()
    for question in questions:
        await ask_async(question)
    sequential = time.perf_counter() - start

    start = time.perf_counter()
    await asyncio.gather(*(ask_async(q) for q in questions))
    concurrent = time.perf_counter() - start

    print(f"sequential : {sequential:.2f}s")
    print(f"concurrent : {concurrent:.2f}s")
    print(f"speedup    : {sequential / concurrent:.1f}x")


def run_async(coro):
    """Execute a coroutine whether or not a loop is already running."""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        return asyncio.run(coro)

    with concurrent.futures.ThreadPoolExecutor(max_workers=1) as pool:
        return pool.submit(asyncio.run, coro).result()


if __name__ == "__main__":
    run_async(compare_sequential_and_concurrent())

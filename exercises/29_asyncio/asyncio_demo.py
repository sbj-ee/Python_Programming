"""Exercise 29: Asyncio.

Cooperative concurrency on a single thread: coroutines run until they hit
an `await`, at which point the event loop is free to run something else.
This is a third concurrency model alongside threading (27) and
multiprocessing (28) -- best for many concurrent I/O-bound tasks without
the overhead of a thread or process per task.
"""

import asyncio
import time


async def fetch_data(name: str, delay: float) -> str:
    print(f"  {name}: starting, will take {delay}s")
    await asyncio.sleep(delay)  # yields control back to the event loop
    print(f"  {name}: done")
    return f"{name}-result"


async def sequential_fetches() -> list[str]:
    # awaiting one after another: total time is the SUM of each delay
    results = []
    for name, delay in [("A", 0.2), ("B", 0.1), ("C", 0.15)]:
        results.append(await fetch_data(name, delay))
    return results


async def concurrent_fetches() -> list[str]:
    # gather runs all coroutines concurrently: total time is the MAX delay
    return list(
        await asyncio.gather(
            fetch_data("A", 0.2),
            fetch_data("B", 0.1),
            fetch_data("C", 0.15),
        )
    )


class AsyncResource:
    """An async context manager: __aenter__/__aexit__ are the async
    counterparts to __enter__/__exit__, for setup/teardown that itself
    needs to await (e.g. opening a network connection).
    """

    async def __aenter__(self) -> "AsyncResource":
        await asyncio.sleep(0.01)
        print("  resource acquired")
        return self

    async def __aexit__(self, exc_type, exc_value, traceback) -> bool:
        await asyncio.sleep(0.01)
        print("  resource released")
        return False


async def async_counter(limit: int):
    """An async generator: combines `yield` with `await`."""
    for i in range(limit):
        await asyncio.sleep(0.01)
        yield i


async def main() -> None:
    print("sequential:")
    start = time.perf_counter()
    seq_results = await sequential_fetches()
    print(f"  total: {time.perf_counter() - start:.2f}s, results={seq_results}")

    print("concurrent:")
    start = time.perf_counter()
    conc_results = await concurrent_fetches()
    print(f"  total: {time.perf_counter() - start:.2f}s, results={conc_results}")

    async with AsyncResource():
        print("  using the resource")

    values = [v async for v in async_counter(5)]
    print(f"async generator values: {values}")

    # --- Task: schedules a coroutine to run concurrently, returns immediately ---
    task = asyncio.create_task(fetch_data("background", 0.1))
    print("did other work while 'background' task runs...")
    result = await task  # wait for it when the result is actually needed
    print(f"background task result: {result}")

    # --- Timeout: cancel a coroutine that takes too long ---
    try:
        async with asyncio.timeout(0.05):
            await fetch_data("too-slow", 0.5)
    except TimeoutError:
        print("caught TimeoutError: 'too-slow' was cancelled")


if __name__ == "__main__":
    asyncio.run(main())

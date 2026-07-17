# Asyncio

Cooperative, single-threaded concurrency: coroutines voluntarily yield
control at each `await`, and the event loop runs something else while
waiting. This is a third concurrency model alongside [[concurrency]]
(threads) and [[multiprocessing]] (processes) — well suited to many
concurrent I/O-bound tasks without a thread or process per task.

## Coroutines and await

```python
import asyncio

async def fetch(name, delay):
    print(f"{name}: starting")
    await asyncio.sleep(delay)   # yields control back to the event loop
    print(f"{name}: done")
    return f"{name}-result"

async def main():
    result = await fetch("A", 1)   # calling a coroutine doesn't run it --
                                     # await does

asyncio.run(main())                 # the entry point: starts the event loop
```

Calling `fetch("A", 1)` alone produces a coroutine object and runs nothing;
only `await`ing it (or scheduling it as a task) actually executes the body.

## Sequential vs. concurrent awaiting

```python
# Sequential: total time = SUM of delays
async def sequential():
    a = await fetch("A", 1)
    b = await fetch("B", 1)
    return [a, b]                # ~2 seconds total

# Concurrent: total time = MAX of delays
async def concurrent():
    return await asyncio.gather(
        fetch("A", 1),
        fetch("B", 1),
    )                              # ~1 second total
```

## Tasks: schedule now, await later

```python
async def main():
    task = asyncio.create_task(fetch("background", 2))   # starts running immediately
    do_other_work()                                        # runs while task is in flight
    result = await task                                     # wait only when needed
```

`asyncio.gather` and `asyncio.create_task` both run coroutines concurrently;
`gather` is for "run these and wait for all of them here," `create_task` is
for "start this now, I'll collect the result later."

## Async context managers and iterators

```python
class Connection:
    async def __aenter__(self):
        await self.connect()
        return self
    async def __aexit__(self, *exc_info):
        await self.disconnect()

async with Connection() as conn:
    await conn.query()

async def counter(limit):
    for i in range(limit):
        await asyncio.sleep(0.1)
        yield i

async for value in counter(5):
    print(value)
```

## Timeouts and cancellation

```python
try:
    async with asyncio.timeout(2.0):
        await fetch("slow", 5)
except TimeoutError:
    print("gave up after 2 seconds")
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Calling a coroutine without `await` or `create_task` | Nothing runs -- "coroutine was never awaited" warning | Always `await` it or schedule it with `create_task`/`gather` |
| Blocking I/O or CPU-heavy work inside a coroutine | Freezes the ENTIRE event loop -- every other task stalls | Use `asyncio.to_thread()` or `run_in_executor` for blocking calls |
| Awaiting sequentially when tasks are independent | Total time is additive instead of the max | Use `asyncio.gather()` for independent, concurrent operations |
| Mixing sync and async code carelessly | `RuntimeError: no running event loop`, or accidental blocking | Keep the async call chain async end-to-end from `asyncio.run()` down |
| Not handling task cancellation/exceptions in `gather` | One failed task can silently cancel siblings, or errors get swallowed | Pass `return_exceptions=True` when partial failure should not abort the group |

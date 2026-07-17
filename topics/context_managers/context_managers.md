# Context Managers

The `with` statement guarantees setup and teardown around a block, even if
the block raises an exception — the Python equivalent of C++'s RAII
(Resource Acquisition Is Initialization), implemented via two dunder
methods instead of a destructor.

## The protocol

```python
class Timer:
    def __enter__(self):
        self.start = time.perf_counter()
        return self                        # bound to the `as` target
    def __exit__(self, exc_type, exc_value, traceback):
        self.elapsed = time.perf_counter() - self.start
        return False                        # False/None: let exceptions propagate

with Timer() as t:
    do_work()
print(t.elapsed)
```

`__exit__` runs unconditionally — success, exception, `return`, or `break`
inside the block all trigger it. Returning `True` from `__exit__` suppresses
the exception; almost always you want `False` (or nothing, which is `None`,
also falsy).

## @contextmanager: generator-based context managers

```python
from contextlib import contextmanager

@contextmanager
def acquire_connection(pool):
    conn = pool.get()
    try:
        yield conn          # code before yield = __enter__, code after = __exit__
    finally:
        pool.release(conn)   # runs even if the `with` block raised

with acquire_connection(pool) as conn:
    conn.execute(query)
```

The `try/finally` inside the generator is what guarantees cleanup — without
it, an exception in the `with` block would skip the release entirely.

## The standard library's own context managers

```python
with open("file.txt") as f:      # closes the file automatically
    data = f.read()

with threading.Lock():            # acquires, then releases automatically
    shared_state += 1

import contextlib
with contextlib.suppress(FileNotFoundError):
    os.remove("maybe_missing.txt")   # skip a SPECIFIC exception, no try/except

with contextlib.ExitStack() as stack:
    files = [stack.enter_context(open(f)) for f in filenames]
    # all files closed automatically when the stack unwinds --
    # useful when the number of resources isn't known until runtime
```

## Multiple context managers in one statement

```python
with open("in.txt") as fin, open("out.txt", "w") as fout:
    fout.write(fin.read())
# equivalent to nesting them, but exits in reverse order automatically
```

## Async context managers

```python
class AsyncResource:
    async def __aenter__(self):
        await self.connect()
        return self
    async def __aexit__(self, exc_type, exc_value, traceback):
        await self.disconnect()
        return False

async with AsyncResource() as r:
    await r.query()
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Forgetting `try/finally` inside a `@contextmanager` generator | An exception in the `with` block skips cleanup | Always wrap the `yield` in `try/finally` |
| Returning `True` from `__exit__` unintentionally | Silently swallows exceptions from the `with` block | Return `False`/`None` unless suppression is deliberate |
| Manual `open()`/`close()` instead of `with open(...)` | A leaked file handle if an exception occurs between them | Always prefer `with` for anything with a `close()`/`release()` |
| Using a context manager object across multiple `with` blocks concurrently | Some (e.g. many DB connections) aren't reentrant -- state corruption | Create a fresh instance per `with`, or confirm reentrancy is supported |
| Mixing `async with` and `with` for the same resource type by mistake | `TypeError`: object does not support the protocol used | Match sync/async context managers to sync/async call sites |

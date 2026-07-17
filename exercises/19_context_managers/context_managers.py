"""Exercise 19: Context Managers.

The `with` statement guarantees setup/teardown around a block, even if the
block raises. A context manager implements __enter__/__exit__, or is built
from a generator with @contextlib.contextmanager.
"""

import time
from contextlib import contextmanager, suppress
from dataclasses import dataclass, field


class Timer:
    """A class-based context manager: __enter__ runs at `with` entry,
    __exit__ runs at exit — success, exception, or otherwise.
    """

    def __enter__(self) -> "Timer":
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc_value, traceback) -> None:
        self.elapsed = time.perf_counter() - self.start
        print(f"  elapsed: {self.elapsed * 1000:.3f}ms")
        # Returning None (falsy) lets any exception propagate normally;
        # only returning True would suppress it.


@dataclass
class ConnectionPool:
    """Simulates a resource pool that must track active/available connections."""

    available: list[str] = field(default_factory=lambda: ["conn-1", "conn-2"])
    in_use: list[str] = field(default_factory=list)

    @contextmanager
    def acquire(self):
        """@contextmanager turns a generator into a context manager: code
        before `yield` is __enter__, code after is __exit__. A `finally` in
        the generator guarantees the connection is released even on error.
        """
        if not self.available:
            raise RuntimeError("no connections available")
        conn = self.available.pop()
        self.in_use.append(conn)
        try:
            yield conn
        finally:
            self.in_use.remove(conn)
            self.available.append(conn)


def main() -> None:
    with Timer() as t:
        total = sum(range(1_000_000))
    print(f"sum = {total}, timer object still usable: {t.elapsed > 0}")

    pool = ConnectionPool()
    print(f"before: available={pool.available}")
    with pool.acquire() as conn:
        print(f"  using {conn}; available={pool.available}, in_use={pool.in_use}")
    print(f"after: available={pool.available}, in_use={pool.in_use}")

    # --- Cleanup still runs even when the block raises ---
    try:
        with pool.acquire() as conn:
            print(f"  using {conn}, about to fail")
            raise ValueError("simulated failure")
    except ValueError as e:
        print(f"caught: {e}")
    print(f"pool recovered: available={pool.available}, in_use={pool.in_use}")

    # --- contextlib.suppress: skip a specific exception without try/except ---
    empty: dict[str, int] = {}
    with suppress(KeyError):
        empty["missing"]
    print("suppress(KeyError) let us continue past the missing-key access")

    # --- Multiple context managers in one `with` ---
    with Timer() as t1, pool.acquire() as c1:
        print(f"  nested: {c1}")
    print(f"nested block elapsed: {t1.elapsed >= 0}")


if __name__ == "__main__":
    main()

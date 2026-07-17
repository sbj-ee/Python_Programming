"""Exercise 27: Threading.

CPython's Global Interpreter Lock (GIL) allows only one thread to execute
Python bytecode at a time. Threads still help with I/O-bound work (network,
disk, sleep) because the GIL is released during blocking I/O -- but they do
NOT give CPU-bound code true parallelism. Exercise 28 (multiprocessing)
covers the CPU-bound case.
"""

import threading
import time
from concurrent.futures import ThreadPoolExecutor
from queue import Queue


def io_bound_task(task_id: int) -> str:
    time.sleep(0.1)  # simulates a network call; GIL is released during sleep
    return f"task {task_id} done"


def cpu_bound_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


class SharedCounter:
    """Demonstrates why a lock is necessary even under the GIL: `+= 1` is
    not atomic -- it is read, add, write, and a thread switch can happen
    between any of those steps.
    """

    def __init__(self) -> None:
        self.value = 0
        self._lock = threading.Lock()

    def increment(self) -> None:
        with self._lock:  # without this, concurrent increments can be lost
            self.value += 1


def main() -> None:
    # --- Threads for I/O-bound work: real wall-clock speedup ---
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        results = list(pool.map(io_bound_task, range(8)))
    elapsed = time.perf_counter() - start
    print(f"8 io_bound_task calls via 4 threads: {elapsed:.2f}s (vs ~0.8s serial)")
    print(f"results[0] = {results[0]}")

    # --- Threads for CPU-bound work: little to no speedup, due to the GIL ---
    start = time.perf_counter()
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(cpu_bound_task, [2_000_000] * 4))
    elapsed = time.perf_counter() - start
    print(f"4 cpu_bound_task calls via 4 threads: {elapsed:.2f}s (GIL serializes this)")

    # --- Race condition without a lock, then the fix ---
    unsafe = {"value": 0}

    def unsafe_increment() -> None:
        for _ in range(100_000):
            unsafe["value"] += 1  # not atomic -- races under contention

    threads = [threading.Thread(target=unsafe_increment) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"unsafe counter after 4x100,000 increments: {unsafe['value']} (expected 400000)")

    safe = SharedCounter()

    def safe_increment() -> None:
        for _ in range(100_000):
            safe.increment()

    threads = [threading.Thread(target=safe_increment) for _ in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    print(f"lock-protected counter: {safe.value} (always exactly 400000)")

    # --- queue.Queue: thread-safe producer/consumer coordination ---
    work_queue: Queue[int | None] = Queue()
    results_list: list[int] = []

    def worker() -> None:
        while True:
            item = work_queue.get()
            if item is None:  # sentinel value signals "stop"
                break
            results_list.append(item * item)
            work_queue.task_done()

    producer_thread = threading.Thread(target=worker)
    producer_thread.start()
    for i in range(5):
        work_queue.put(i)
    work_queue.put(None)  # tell the worker to stop
    producer_thread.join()
    print(f"queue-driven results: {sorted(results_list)}")


if __name__ == "__main__":
    main()

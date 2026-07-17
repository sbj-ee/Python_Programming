"""Exercise 28: Multiprocessing.

Each process gets its own Python interpreter and its own GIL, so
multiprocessing achieves real parallelism for CPU-bound work -- at the cost
of higher memory use and the need to explicitly share state (processes do
not share memory by default, unlike threads).
"""

import time
from multiprocessing import Pool, Process, Queue, Value
from multiprocessing.sharedctypes import SynchronizedBase


def cpu_bound_task(n: int) -> int:
    total = 0
    for i in range(n):
        total += i * i
    return total


def worker_with_queue(worker_id: int, q: "Queue[str]") -> None:
    q.put(f"worker {worker_id} finished")


def increment_shared(counter: SynchronizedBase) -> None:
    for _ in range(10_000):
        with counter.get_lock():  # explicit lock: processes need it too
            counter.value += 1  # type: ignore[attr-defined]  # imprecise stub for the generic ctype


def main() -> None:
    # `if __name__ == "__main__":` is REQUIRED before spawning processes on
    # macOS/Windows (spawn start method) -- each child re-imports this
    # module, and without the guard it would re-run main() recursively.

    # --- Real parallel speedup for CPU-bound work ---
    start = time.perf_counter()
    for _ in range(4):
        cpu_bound_task(2_000_000)
    serial_time = time.perf_counter() - start
    print(f"serial (4x): {serial_time:.2f}s")

    start = time.perf_counter()
    with Pool(processes=4) as pool:
        pool.map(cpu_bound_task, [2_000_000] * 4)
    parallel_time = time.perf_counter() - start
    print(f"parallel (Pool, 4 processes): {parallel_time:.2f}s")
    print(f"speedup: {serial_time / parallel_time:.2f}x")

    # --- Process + Queue: explicit message passing between processes ---
    q: Queue[str] = Queue()
    processes = [Process(target=worker_with_queue, args=(i, q)) for i in range(3)]
    for p in processes:
        p.start()
    for p in processes:
        p.join()
    messages = sorted(q.get() for _ in range(3))
    print(f"messages from workers: {messages}")

    # --- Value: shared memory for a single primitive, with its own lock ---
    counter = Value("i", 0)  # 'i' = C int
    procs = [Process(target=increment_shared, args=(counter,)) for _ in range(4)]
    for p in procs:
        p.start()
    for p in procs:
        p.join()
    print(f"shared counter after 4x10,000 increments: {counter.value} (expected 40000)")


if __name__ == "__main__":
    main()

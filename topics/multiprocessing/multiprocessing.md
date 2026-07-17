# Multiprocessing

Each process gets its own Python interpreter and its own GIL, so
`multiprocessing` achieves genuine parallelism for CPU-bound work — unlike
[[concurrency]] (threading), which is serialized by the GIL for pure-Python
bytecode. The cost: processes don't share memory by default, so data must
be explicitly serialized (pickled) and passed between them.

## Pool: the common case

```python
from multiprocessing import Pool

def cpu_bound_task(n):
    return sum(i * i for i in range(n))

if __name__ == "__main__":   # REQUIRED on macOS/Windows before spawning
    with Pool(processes=4) as pool:
        results = pool.map(cpu_bound_task, [10**6] * 4)   # runs in parallel
```

The `if __name__ == "__main__":` guard is not optional here on platforms
using the "spawn" start method (macOS, Windows, and Linux since Python
3.14's imminent default change): each child process re-imports this module
from scratch, and without the guard, importing it would re-trigger process
creation recursively.

## Process and explicit message passing

```python
from multiprocessing import Process, Queue

def worker(worker_id, q):
    q.put(f"worker {worker_id} done")

if __name__ == "__main__":
    q = Queue()
    procs = [Process(target=worker, args=(i, q)) for i in range(3)]
    for p in procs: p.start()
    for p in procs: p.join()
    messages = [q.get() for _ in range(3)]
```

## Sharing state: Value, Array, and locks

```python
from multiprocessing import Process, Value

def increment(counter):
    for _ in range(10_000):
        with counter.get_lock():    # processes need explicit locking too --
            counter.value += 1       # shared memory does NOT make += atomic

if __name__ == "__main__":
    counter = Value("i", 0)          # 'i' = C int, allocated in shared memory
    procs = [Process(target=increment, args=(counter,)) for _ in range(4)]
    for p in procs: p.start()
    for p in procs: p.join()
```

Most data passed between processes (via `Queue`, `Pool.map` arguments and
return values) is pickled, sent, and unpickled — not shared memory. `Value`
and `Array` are the exception: real shared memory, backed by explicit locks.

## Choosing threads vs. processes vs. asyncio

| Workload | Best fit | Why |
|----------|----------|-----|
| CPU-bound (number crunching, image processing) | `multiprocessing` | Bypasses the GIL entirely -- true parallel cores |
| I/O-bound, moderate concurrency (dozens of connections) | `threading` | Simple, GIL releases during I/O, low overhead per task |
| I/O-bound, high concurrency (thousands of connections) | `asyncio` | No per-task thread/process overhead, single-threaded event loop |

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Missing `if __name__ == "__main__":` guard | Infinite process spawning / `RuntimeError` on macOS/Windows | Always guard multiprocessing entry points |
| Passing unpicklable objects (open file handles, lambdas, DB connections) to a `Process`/`Pool` | `PicklingError` | Pass simple/serializable data; open resources inside the child instead |
| Assuming processes share memory like threads do | Changes in one process are invisible to others | Use `Value`/`Array`/`shared_memory`, or pass data explicitly via `Queue` |
| High process-creation overhead for small, frequent tasks | Slower than just doing it in one process | Batch work per task, or use a persistent `Pool` instead of spawning per call |
| Forgetting a lock around a shared `Value`/`Array` | Lost updates under contention, same as unprotected threads | `with shared_value.get_lock():` around read-modify-write |

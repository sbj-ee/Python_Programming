# Concurrency (Threading)

CPython's Global Interpreter Lock (GIL) allows only one thread to execute
Python bytecode at a time. Threads still help for I/O-bound work — the GIL
is released during blocking system calls (file I/O, network, `time.sleep`)
— but they give no speedup for CPU-bound pure-Python code. See
[[multiprocessing]] for the CPU-bound answer.

## Creating threads

```python
import threading

def worker(name):
    print(f"{name} starting")

t = threading.Thread(target=worker, args=("thread-1",))
t.start()
t.join()               # block until the thread finishes

# Higher-level: a pool that manages threads for you
from concurrent.futures import ThreadPoolExecutor

with ThreadPoolExecutor(max_workers=4) as pool:
    results = list(pool.map(fetch_url, urls))   # runs concurrently, I/O-bound
```

## Why I/O-bound work benefits, CPU-bound work doesn't

```python
# I/O-bound: the GIL is released during time.sleep()/socket calls, so
# 4 threads sleeping 1s each finish in ~1s total, not 4s.
def io_task():
    time.sleep(1)

# CPU-bound: pure Python bytecode execution holds the GIL the whole time.
# 4 threads doing this take roughly the SAME total time as 1 thread --
# no parallelism, only the overhead of context-switching between them.
def cpu_task(n):
    total = 0
    for i in range(n):
        total += i * i
    return total
```

## Locks: protecting shared, mutable state

```python
counter = 0
lock = threading.Lock()

def increment():
    global counter
    for _ in range(100_000):
        with lock:              # without this, concurrent += 1 loses updates
            counter += 1         # read-modify-write is NOT atomic in Python
```

`counter += 1` looks like one operation but is actually three (read, add,
write), and a thread switch can land between any of them. The GIL prevents
data corruption at the bytecode level but does NOT make compound operations
like `+=` atomic — a lock is still required for correctness.

## queue.Queue: thread-safe producer/consumer

```python
from queue import Queue

q = Queue()

def producer():
    for i in range(5):
        q.put(i)
    q.put(None)          # sentinel: tells the consumer to stop

def consumer():
    while (item := q.get()) is not None:
        process(item)
        q.task_done()
```

`queue.Queue` handles its own internal locking — it is the idiomatic way to
hand data between threads without managing a `Lock` by hand.

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Expecting threads to speed up CPU-bound Python | No speedup -- the GIL serializes bytecode execution | Use `multiprocessing` for CPU-bound parallelism |
| `counter += 1` from multiple threads without a lock | Lost updates -- final count is less than expected | Wrap the read-modify-write in `with lock:` |
| Forgetting `t.join()` | Main program may exit before the thread finishes | Always `join()` threads you need to complete, or use a pool's context manager |
| Deadlock from acquiring locks in inconsistent order across threads | Program hangs forever | Always acquire multiple locks in the same, fixed order everywhere |
| Sharing mutable objects across threads without synchronization | Data races, corrupted state | Protect shared state with a `Lock`, or hand data through `queue.Queue` instead |

# Python Programming

*Topics: python, learning, education, systems-programming, tutorial, exercises*

A structured Python learning project covering fundamentals through systems programming.

## Layout

```
Python_Programming/
├── Foreword.md      # Guido van Rossum, the PEP process, CPython, and the GIL
├── Introduction.md  # Dev environment, exercise progression, key differences from C/C++
├── exercises/       # Progressive scripts, each building on the last
│   ├── 01_hello_world/ … 33_regex/
└── topics/              # Markdown reference sheets by concept
    ├── types/                numeric tower, mutability, truthiness, casting
    ├── references/           name binding, is vs ==, copy/deepcopy, GC
    ├── collections/          list/tuple/dict/set, comprehensions, collections module
    ├── strings/              str methods, f-strings, str vs bytes, slicing
    ├── functions/            *args/**kwargs, closures, functools, recursion
    ├── decorators/           function/class decorators, functools.wraps, factories
    ├── classes/               dataclasses, properties, __slots__, dunder methods
    ├── inheritance/          MRO, super(), ABCs, mixins
    ├── typing/               type hints, generics, Protocol, mypy workflow
    ├── error_handling/       exceptions, custom hierarchies, chaining, exception groups
    ├── generators/           yield, generator expressions, itertools, iterator protocol
    ├── context_managers/     with statement, @contextmanager, ExitStack
    ├── file_io/              pathlib, open(), json, csv
    ├── modules_and_packages/ import system, __init__.py, sys.path, relative imports
    ├── testing/               pytest fixtures, parametrize, monkeypatch, mocking
    ├── concurrency/          threading, the GIL, locks, ThreadPoolExecutor
    ├── asyncio/               event loop, async/await, tasks, gather, timeouts
    ├── multiprocessing/       Process, Pool, Queue, shared memory
    ├── processes/             subprocess, pipes, os.fork/exec (POSIX)
    ├── sockets/               TCP/UDP, send/recv discipline, getaddrinfo
    ├── regex/                 re module, groups, sub, compiled patterns
    └── dynamic_loading/       importlib, plugin pattern, entry points
```

## Setup

```bash
# This project uses uv
uv venv
uv sync

# Or with plain venv + pip
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running

```bash
# Run a single exercise
python3 exercises/01_hello_world/hello.py
uv run exercises/17_decorators/decorators.py

# Run the test suite
uv run pytest

# Lint
uv run ruff check .

# Type-check
uv run mypy exercises topics
```

## Requirements

- Python 3.11+ (3.12+ recommended)
- `uv` (recommended) or `pip` + `venv`

## Exercises

| # | Topic | Concepts |
|---|-------|----------|
| 01 | Hello World | `print`, comments, running a script |
| 02 | Variables & Types | dynamic typing, `int`/`float`/`str`/`bool`, `type()`, casting |
| 03 | Control Flow | `if/elif/else`, `for`/`while`, `match`, comprehensions |
| 04 | Functions | `def`, `*args`/`**kwargs`, default args, docstrings, recursion |
| 05 | Strings & Lists | `str` methods, f-strings, list methods, slicing |
| 06 | Dicts & Sets | `dict`, `set`, comprehensions, `Counter`, `defaultdict` |
| 07 | References & Mutability | `id()`, `is` vs `==`, aliasing, mutable-default-argument trap |
| 08 | Classes | `class`, `__init__`, instance vs. class attributes, methods |
| 09 | File I/O | `open()`, `pathlib.Path`, context managers, `json`/`csv` |
| 10 | Linked Lists | singly linked list, traversal, comparison with `collections.deque` |
| 11 | Closures & Higher-Order Functions | first-class functions, closures, `map`/`filter`/`reduce` |
| 12 | Dataclasses & Enums | `@dataclass`, `Enum`, `NamedTuple` |
| 13 | Operator Overloading | `__eq__`, `__lt__`, `__add__`, `__repr__`, `__hash__` |
| 14 | Inheritance | single/multiple inheritance, `super()`, MRO |
| 15 | ABCs & Protocols | `abc.ABC`, `@abstractmethod`, `typing.Protocol`, structural typing |
| 16 | Exceptions | `try`/`except`/`else`/`finally`, custom exceptions, `raise ... from`, exception groups |
| 17 | Decorators | function decorators, `functools.wraps`, parametrized decorators |
| 18 | Generators & Iterators | `yield`, `__iter__`/`__next__`, generator expressions, `itertools` |
| 19 | Context Managers | `with`, `contextlib.contextmanager`, `__enter__`/`__exit__` |
| 20 | Typing & Generics | type hints, `Optional`, `Union`, `TypeVar`, generics, `mypy` |
| 21 | Modules & Packages | imports, `__init__.py`, `__name__ == "__main__"`, relative imports |
| 22 | Testing with pytest | fixtures, `parametrize`, `monkeypatch`, mocking |
| 23 | Binary Search Tree | insert, search, delete (3 cases), traversals, height |
| 24 | Stack & Queue | LIFO/FIFO via `collections.deque`, bracket balancing, BFS |
| 25 | Sorting & Searching | bubble/insertion/merge/quicksort, `sorted()`, `bisect` |
| 26 | Hash Table | separate chaining from scratch, compared with `dict` |
| 27 | Threading | `threading.Thread`, the GIL, `Lock`, `ThreadPoolExecutor` |
| 28 | Multiprocessing | `Process`, `Pool`, `Queue`, shared memory (`Value`) |
| 29 | Asyncio | `async`/`await`, event loop, `asyncio.gather`, async context managers |
| 30 | Processes | `subprocess`, pipes, `os.fork`/`exec` (POSIX only) |
| 31 | Sockets | TCP/UDP client and server, `send_all`/`recv_exactly` |
| 32 | I/O Multiplexing | `selectors`, non-blocking sockets, multi-client echo server |
| 33 | Regex | `re` — `match`/`search`/`findall`, groups, compiled patterns, `sub` |

---

## Appendix: Tooling

This project uses [`uv`](https://github.com/astral-sh/uv) for environment and
dependency management, [`ruff`](https://github.com/astral-sh/ruff) for
linting, and [`mypy`](https://mypy-lang.org/) for static type checking. All
three are declared as dev dependencies in `pyproject.toml`.

```toml
[tool.ruff]
line-length = 100
target-version = "py311"

[tool.ruff.lint]
select = ["E", "F", "W", "I", "UP", "B"]
```

| Tool | Purpose |
|------|---------|
| `pytest` | Test runner — used directly by exercise 22, available for all others |
| `ruff` | Linting + import sorting + pyupgrade-style modernization, in one fast tool |
| `mypy` | Static type checking against the hints used throughout, especially exercise 20 |

## Key Differences from C_Programming / CPP_Programming

| Concern | C / C++ | Python |
|---------|---------|--------|
| Compilation | `gcc`/`g++` to a binary | Interpreted (compiled to bytecode at import) |
| Typing | Static, checked at compile time | Dynamic; optional static hints checked by `mypy` |
| Memory | Manual (`malloc`/`free`) or RAII | Reference counting + cycle-detecting garbage collector |
| Generics | `void *`/macros or templates | Duck typing; `typing.Generic`/`TypeVar` for hints only |
| Concurrency | OS threads, true parallelism | GIL limits CPU-bound threads; `multiprocessing` or `asyncio` for real concurrency |
| Error handling | Return codes / exceptions | Exceptions are the primary and idiomatic mechanism |
| Build system | `make`/`Makefile` | None — scripts run directly; `pyproject.toml` for dependencies |

See `Introduction.md` for the full exercise-by-exercise progression and tier breakdown.

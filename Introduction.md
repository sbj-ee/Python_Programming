# Introduction

## Who This Is For

This project is for programmers who already know how to code — in C, C++, or
another language — and want a structured path through idiomatic Python, from
syntax through systems programming. It assumes you can read a function and
write a loop. It does not assume prior Python experience.

If you have worked through `C_Programming` or `CPP_Programming`, several
exercises here (linked lists, sorting, hash tables, threading, sockets,
regex) will feel familiar in shape. What changes is the idiom: Python trades
manual memory management and compile-time types for a garbage collector,
dynamic typing, and a standard library deep enough that most of these
exercises need no third-party packages at all.

## Philosophy

Each exercise is a self-contained script that runs top to bottom and prints
observable output. There are no stub files to fill in. Read the source, run
it, then change something. Understanding comes from reading and breaking
working code, not from filling in blanks.

Comments in the exercises explain the *why*, not the *what*. The code itself
explains the what.

## Development Environment

```bash
# Interpreter
python3 --version   # 3.11+ required; 3.12+ recommended

# Environment and package management (this project uses uv)
uv --version

# Fallback if you prefer the stdlib tools
python3 -m venv --help
pip --version
```

### Setup

```bash
# Create and sync the virtual environment (installs pytest, ruff, mypy)
uv venv
uv sync

# Or with plain venv + pip
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Running Exercises

```bash
# Run a single exercise directly
python3 exercises/01_hello_world/hello.py

# Run with uv (uses the project's synced environment)
uv run exercises/08_classes/classes.py

# Run the test suite (covers exercises that define tests, e.g. 22, 26)
uv run pytest

# Lint everything
uv run ruff check .

# Type-check
uv run mypy exercises topics
```

Every exercise is one Python file (occasionally a small package for the
multi-module exercises) that runs standalone — no build step, no Makefile.
`if __name__ == "__main__":` guards the demonstration code in every file, so
each script can also be imported without side effects.

## Exercise Progression

The 33 exercises form five progressive tiers.

### Tier 1 — Python Fundamentals (01–09)

| # | Topic | Core Idea |
|---|-------|-----------|
| 01 | Hello World | `print`, comments, running a script |
| 02 | Variables & Types | dynamic typing, `int`/`float`/`str`/`bool`, `type()`, casting |
| 03 | Control Flow | `if`/`elif`/`else`, `for`/`while`, `match`, comprehensions |
| 04 | Functions | `def`, `*args`/`**kwargs`, default arguments, docstrings, recursion |
| 05 | Strings & Lists | `str` methods, f-strings, list methods, slicing |
| 06 | Dicts & Sets | `dict`, `set`, comprehensions, `Counter`, `defaultdict` |
| 07 | References & Mutability | `id()`, `is` vs `==`, aliasing, the mutable-default-argument trap |
| 08 | Classes | `class`, `__init__`, instance vs. class attributes, methods |
| 09 | File I/O | `open()`, `pathlib.Path`, context managers, `json`/`csv` |

### Tier 2 — Object-Oriented & Functional Python (10–18)

| # | Topic | Core Idea |
|---|-------|-----------|
| 10 | Linked Lists | singly linked list class; comparison with `collections.deque` |
| 11 | Closures & Higher-Order Functions | first-class functions, closures, `map`/`filter`/`functools.reduce` |
| 12 | Dataclasses & Enums | `@dataclass`, `Enum`, `NamedTuple` |
| 13 | Operator Overloading | `__eq__`, `__lt__`, `__add__`, `__repr__`, `__hash__` |
| 14 | Inheritance | single/multiple inheritance, `super()`, MRO (Method Resolution Order) |
| 15 | ABCs & Protocols | `abc.ABC`, `@abstractmethod`, `typing.Protocol`, structural typing |
| 16 | Exceptions | `try`/`except`/`else`/`finally`, custom exceptions, `raise ... from`, exception groups |
| 17 | Decorators | function decorators, `functools.wraps`, parametrized decorators |
| 18 | Generators & Iterators | `yield`, `__iter__`/`__next__`, generator expressions, `itertools` |

### Tier 3 — Modern Python Idioms (19–22)

| # | Topic | Core Idea |
|---|-------|-----------|
| 19 | Context Managers | `with`, `contextlib.contextmanager`, `__enter__`/`__exit__` |
| 20 | Typing & Generics | type hints, `Optional`, `Union`, `TypeVar`, generics, `mypy` |
| 21 | Modules & Packages | imports, `__init__.py`, `__name__ == "__main__"`, relative imports |
| 22 | Testing with pytest | fixtures, `parametrize`, `monkeypatch`, assertion introspection |

### Tier 4 — Data Structures & Algorithms (23–26)

| # | Topic | Core Idea |
|---|-------|-----------|
| 23 | Binary Search Tree | insert, search, delete (3 cases), traversals, height |
| 24 | Stack & Queue | LIFO/FIFO with `collections.deque`, bracket balancing, BFS |
| 25 | Sorting & Searching | bubble/insertion/merge/quicksort, `sorted()`, `bisect` |
| 26 | Hash Table | separate chaining from scratch, compared with `dict` |

### Tier 5 — Systems & Concurrent Python (27–33)

| # | Topic | Core Idea |
|---|-------|-----------|
| 27 | Threading | `threading.Thread`, the GIL, `Lock`, `ThreadPoolExecutor` |
| 28 | Multiprocessing | `Process`, `Pool`, `Queue`, shared memory |
| 29 | Asyncio | `async`/`await`, the event loop, `asyncio.gather`, async context managers |
| 30 | Processes | `subprocess`, pipes, `os.fork`/`exec` (POSIX only) |
| 31 | Sockets | TCP/UDP client and server with the `socket` module |
| 32 | I/O Multiplexing | `selectors`, non-blocking sockets, a multi-client echo server |
| 33 | Regex | `re` — `match`/`search`/`findall`, groups, compiled patterns |

## Key Differences from C_Programming / CPP_Programming

The C and C++ projects cover overlapping systems topics. Here is what changes
in Python:

| Concern | C / C++ | Python |
|---------|---------|--------|
| Compilation | `gcc`/`g++` to a binary | Interpreted (compiled to bytecode at import) |
| Typing | Static, checked at compile time | Dynamic; optional static hints checked by `mypy` |
| Memory | Manual (`malloc`/`free`) or RAII | Reference counting + cycle-detecting garbage collector |
| Generics | `void *`/macros or templates | Duck typing; `typing.Generic`/`TypeVar` for hints only |
| Concurrency | OS threads, true parallelism | GIL limits CPU-bound threads; `multiprocessing` or `asyncio` for real concurrency |
| Error handling | Return codes / exceptions | Exceptions are the primary and idiomatic mechanism |
| Build system | `make`/`Makefile` | None — scripts run directly; `pyproject.toml` for dependencies |

## Every File Has

- A single `.py` source file (or small package) with clearly commented sections
- An `if __name__ == "__main__":` block producing runnable, observable output
- Zero `ruff` warnings under this project's configuration
- Type hints on function signatures, checked with `mypy` where practical

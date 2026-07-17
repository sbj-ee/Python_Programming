# Typing

Type hints are optional, unenforced at runtime, and read by external tools
like `mypy` or `pyright`. Python remains fully dynamically typed — hints are
documentation that a checker can verify, not a runtime contract.

## Basic hints

```python
def add(a: int, b: int) -> int:
    return a + b

name: str = "Ada"
scores: list[float] = [9.5, 8.0]
lookup: dict[str, int] = {"a": 1}

add("x", "y")   # runs fine at runtime; mypy would flag it as an error
```

## Optional and Union

```python
from typing import Optional, Union

def find(items: list[int], target: int) -> Optional[int]:
    # Optional[int] means Union[int, None] -- "an int, or nothing"
    return items.index(target) if target in items else None

def describe(value: Union[int, str]) -> str:
    return str(value)

# Python 3.10+ prefers the | syntax over typing.Optional/Union:
def find_modern(items: list[int], target: int) -> int | None: ...
def describe_modern(value: int | str) -> str: ...
```

## Generics

```python
from typing import TypeVar, Generic

T = TypeVar("T")

def first(items: list[T]) -> T:
    return items[0]

class Stack(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []
    def push(self, item: T) -> None:
        self._items.append(item)
    def pop(self) -> T:
        return self._items.pop()

int_stack: Stack[int] = Stack()    # mypy tracks that this holds only ints
```

## Protocol: structural typing

```python
from typing import Protocol

class HasArea(Protocol):
    def area(self) -> float: ...

def total_area(shapes: list[HasArea]) -> float:
    return sum(s.area() for s in shapes)

# ANY object with an area() method satisfies HasArea -- no inheritance
# required. This is Python's version of duck typing, checkable statically.
```

## TypedDict and NewType

```python
from typing import TypedDict, NewType

class UserRecord(TypedDict):
    name: str
    age: int

record: UserRecord = {"name": "Ada", "age": 36}   # checked shape, still a plain dict

UserId = NewType("UserId", int)   # a distinct type to mypy, same as int at runtime
def get_user(user_id: UserId) -> UserRecord: ...
```

## Running a checker

```bash
mypy my_module.py
mypy --strict my_module.py    # much stricter: no implicit Optional, etc.
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Assuming hints are enforced at runtime | Wrong types pass silently until they cause a real error elsewhere | Run `mypy`/`pyright` in CI; hints alone check nothing |
| Using `typing.Optional[X]` without a default of `None` | mypy still requires callers to handle the `None` case | Handle `None` explicitly wherever the value is used |
| Circular imports caused by type-only imports | `ImportError` at runtime | `from __future__ import annotations`, or `if TYPE_CHECKING:` guard |
| Overusing `Any` to silence errors | Defeats the purpose of static checking | Narrow with `Union`/`Protocol`/`TypeVar` instead where feasible |
| Forgetting generic parameters (`list` instead of `list[int]`) | Loses element-type checking | Always parametrize built-in generics when the element type is known |

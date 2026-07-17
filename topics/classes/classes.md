# Classes

`class` defines a blueprint for objects. `@dataclass` generates the
boilerplate (`__init__`, `__repr__`, `__eq__`) for classes that are mostly
data, and dunder methods control how instances behave with built-in
operators and functions.

## The basics

```python
class Counter:
    total_created = 0            # class attribute: shared across instances

    def __init__(self, start=0):
        self.value = start        # instance attribute: unique per object
        Counter.total_created += 1

    def increment(self, by=1):
        self.value += by

c1 = Counter()
c2 = Counter(start=10)
Counter.total_created   # 2

c1.total_created = "shadowed"   # creates an INSTANCE attribute of the
                                  # same name -- Counter.total_created
                                  # is untouched, but c1.total_created hides it
```

## @dataclass: less boilerplate for data-holding classes

```python
from dataclasses import dataclass, field

@dataclass
class Task:
    title: str
    done: bool = False
    tags: list[str] = field(default_factory=list)   # safe mutable default

# __init__, __repr__, and __eq__ are generated automatically:
t1 = Task("write docs")
t2 = Task("write docs")
t1 == t2      # True -- field-by-field comparison, not identity

@dataclass(frozen=True)
class Point:
    x: float
    y: float
# frozen=True makes instances immutable AND hashable -- usable as dict keys
```

## Properties: computed attributes with attribute syntax

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

    @area.setter
    def area(self, value):
        self._radius = (value / 3.14159) ** 0.5

c = Circle(2)
c.area          # called like an attribute, computed on access
c.area = 50.0    # invokes the setter
```

## __slots__: trading flexibility for memory

```python
class Point:
    __slots__ = ("x", "y")   # no per-instance __dict__ -- less memory,
                               # faster attribute access, no arbitrary
                               # new attributes ("p.z = 1" raises AttributeError)

    def __init__(self, x, y):
        self.x, self.y = x, y
```

## Key dunder methods

```python
class Vector:
    def __init__(self, x, y): self.x, self.y = x, y
    def __repr__(self): return f"Vector({self.x}, {self.y})"   # for developers
    def __str__(self): return f"({self.x}, {self.y})"           # for print()
    def __eq__(self, other): return (self.x, self.y) == (other.x, other.y)
    def __hash__(self): return hash((self.x, self.y))           # needed if __eq__ is defined
    def __add__(self, other): return Vector(self.x + other.x, self.y + other.y)
    def __len__(self): return 2
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Mutable default in `@dataclass` field (`tags: list = []`) | `TypeError` at class definition time -- dataclass explicitly forbids it | `field(default_factory=list)` |
| Defining `__eq__` without `__hash__` | Instances become unhashable (`__hash__` is set to `None` automatically) | Define `__hash__` explicitly, or use `@dataclass(frozen=True)` |
| Confusing class attributes with instance attributes | Mutating a class-level mutable default affects every instance | Set mutable state in `__init__`, not as a class attribute |
| Forgetting `self` in a method | `TypeError: missing 1 required positional argument` | Every instance method needs `self` as its first parameter |
| No `__slots__` on a class created millions of times | Higher memory use than necessary | Add `__slots__` when the attribute set is fixed and instances are numerous |

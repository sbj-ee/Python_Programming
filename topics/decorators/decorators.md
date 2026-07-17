# Decorators

A decorator is a function that takes a function (or class) and returns a
replacement. `@decorator` above a `def` is syntax sugar for
`func = decorator(func)`, evaluated immediately at definition time.

## The minimal decorator

```python
def shout(func):
    def wrapper(*args, **kwargs):
        result = func(*args, **kwargs)
        return result.upper()
    return wrapper

@shout
def greet(name):
    return f"hello, {name}"

greet("ada")   # "HELLO, ADA"
# equivalent to: greet = shout(greet)
```

## functools.wraps: preserving identity

```python
import functools

def timer(func):
    @functools.wraps(func)      # copies __name__, __doc__, __module__ onto wrapper
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@timer
def slow():
    """Does something slow."""

slow.__name__   # "slow" -- WITHOUT @functools.wraps this would be "wrapper"
```

Skipping `functools.wraps` silently breaks introspection, docs, and
anything relying on `__name__` (logging, debuggers, some test frameworks).
There is essentially no reason to omit it.

## Decorator factories: decorators that take arguments

```python
def retry(times):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(times):
                try:
                    return func(*args, **kwargs)
                except ValueError:
                    if attempt == times - 1:
                        raise
        return wrapper
    return decorator

@retry(times=3)
def flaky():
    ...
# @retry(times=3) calls retry(3) first, which returns `decorator`,
# which is then applied to `flaky` -- three levels of function nesting.
```

## Class decorators

```python
def add_repr(cls):
    def __repr__(self):
        attrs = ", ".join(f"{k}={v!r}" for k, v in self.__dict__.items())
        return f"{cls.__name__}({attrs})"
    cls.__repr__ = __repr__
    return cls

@add_repr
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y
```

## Stacking decorators

```python
@timer
@retry(times=2)
def combined():
    ...
# Applied bottom-up: combined = timer(retry(times=2)(combined))
# Calling combined() runs timer's wrapper first, which calls retry's
# wrapper, which calls the original function.
```

## Built-in decorators you already use

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):                  # accessed like an attribute: c.area
        return 3.14159 * self._radius ** 2

    @staticmethod
    def unit_circle():               # no self or cls
        return Circle(1)

    @classmethod
    def from_diameter(cls, d):       # receives the class, not an instance
        return cls(d / 2)
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Omitting `@functools.wraps` | `__name__`/`__doc__` become the wrapper's, breaking introspection | Always apply `functools.wraps(func)` to the inner `wrapper` |
| Forgetting the extra call level in a decorator factory | `TypeError: decorator() missing 1 required positional argument` | Remember: `@retry(times=3)` needs THREE nested functions, not two |
| A decorator that doesn't return anything | Decorated function becomes `None` | Every decorator must `return wrapper` (or the class) |
| Stacking order confusion | Wrong execution order | Read bottom-up: the closest decorator to `def` wraps first |
| Mutable state shared across calls in a decorator (e.g. a cache dict at module scope) | Unexpected cross-call interference in tests | Scope the state per-decoration, or document it as intentional (e.g. `lru_cache`) |

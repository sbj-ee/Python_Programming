# Functions

Functions are first-class objects in Python: they can be assigned to
variables, passed as arguments, stored in collections, and returned from
other functions.

## Arguments: positional, keyword, default, *args, **kwargs

```python
def greet(name, greeting="Hello"):     # greeting has a default
    return f"{greeting}, {name}!"

greet("Ada")                    # "Hello, Ada!"
greet("Ada", greeting="Hi")     # "Hi, Ada!"
greet(name="Ada", greeting="Hi")

def describe(*args, **kwargs):
    # args: tuple of extra positional args
    # kwargs: dict of extra keyword args
    print(args, kwargs)

describe(1, 2, x="a")           # (1, 2) {'x': 'a'}

numbers = [1, 2, 3]
describe(*numbers)               # unpacks the list as positional args
options = {"x": 1}
describe(**options)              # unpacks the dict as keyword args
```

## Positional-only and keyword-only parameters

```python
def f(a, b, /, c, *, d):
    # a, b: positional-only (cannot be passed by name)
    # c: normal (either)
    # d: keyword-only (must be passed by name)
    return a + b + c + d

f(1, 2, c=3, d=4)     # ok
f(1, 2, 3, d=4)        # also ok -- c can be positional
f(a=1, b=2, c=3, d=4)  # TypeError: a, b are positional-only
```

## Closures

A closure is a function that remembers variables from its enclosing scope.

```python
def make_multiplier(factor):
    def multiplier(x):
        return x * factor    # `factor` is captured from the enclosing scope
    return multiplier

double = make_multiplier(2)
double(5)   # 10

def make_counter():
    count = 0
    def increment():
        nonlocal count       # required to REASSIGN an outer variable
        count += 1
        return count
    return increment
```

Without `nonlocal`, `count += 1` inside `increment` would raise
`UnboundLocalError` — any assignment to a name inside a function makes
Python treat it as local for the ENTIRE function body, unless declared
`nonlocal` (enclosing scope) or `global` (module scope).

## functools: partial, reduce, lru_cache

```python
from functools import partial, reduce, lru_cache

add = lambda a, b: a + b
add_five = partial(add, 5)       # freezes the first argument
add_five(10)                      # 15

reduce(lambda acc, x: acc + x, [1, 2, 3, 4], 0)   # 10

@lru_cache(maxsize=None)
def fib(n):                        # memoized -- repeated calls are O(1)
    return n if n < 2 else fib(n - 1) + fib(n - 2)
```

## Recursion

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)

# Python has no tail-call optimization and a default recursion limit
import sys
sys.getrecursionlimit()   # 1000 by default
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Mutable default argument | Shared state leaks across calls | Default to `None`, create fresh inside |
| Forgetting `nonlocal` when reassigning a closed-over variable | `UnboundLocalError` | Add `nonlocal name` at the top of the inner function |
| Deep recursion | `RecursionError` at the default limit (1000) | Convert to iteration, or raise the limit deliberately with `sys.setrecursionlimit` |
| Late binding in closures inside a loop | All closures see the LAST loop value | `def f(x=x): ...` to capture the value at definition time |
| Overusing `*args, **kwargs` | Hides the real signature from callers and IDEs | Prefer explicit parameters where the shape is known |

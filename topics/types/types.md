# Types

Python is dynamically typed: every value carries its own type at runtime,
and a name can be rebound to a value of any type. There is no compile-time
type checking unless you run a separate tool like `mypy` over type hints.

## The core built-in types

```python
i: int = 42          # arbitrary precision -- no overflow, ever
f: float = 3.14       # C double under the hood (64-bit IEEE 754)
s: str = "text"       # immutable sequence of Unicode code points
b: bool = True        # subclass of int; True == 1, False == 0
n = None              # the single instance of NoneType
c = 3 + 4j             # complex numbers are built in
```

## type() vs isinstance()

```python
type(True) is bool          # True -- exact type
isinstance(True, int)       # True -- bool IS-A int (subclass)
isinstance(True, bool)      # True

# isinstance() respects the class hierarchy; type() does not.
# Prefer isinstance() for type checks -- it works correctly with subclasses.
```

## Mutability

The type determines mutability; there is no separate `const` keyword.

| Immutable | Mutable |
|-----------|---------|
| `int`, `float`, `complex`, `bool` | `list` |
| `str` | `dict` |
| `tuple` | `set` |
| `frozenset` | `bytearray` |
| `bytes` | custom classes (by default) |

```python
t = (1, 2, 3)
t[0] = 99   # TypeError: 'tuple' object does not support item assignment

lst = [1, 2, 3]
lst[0] = 99  # fine -- list is mutable
```

## Truthiness

Every object is usable in a boolean context; `bool(x)` defines the rule.

```python
bool(0), bool(0.0), bool(""), bool([]), bool({}), bool(None)  # all False
bool(1), bool("0"), bool([0]), bool({0: 0})                    # all True

# The literal string "0" is truthy -- only the EMPTY string is falsy.
if my_list:          # idiomatic: "if non-empty" instead of len(my_list) > 0
    ...
```

## Numeric conversions and the numeric tower

```python
int(3.9)      # 3    -- truncates toward zero, does not round
round(3.9)    # 4    -- proper rounding
int("42")     # 42
int("3.5")    # ValueError -- int() does not parse floats from strings
float("3.5")  # 3.5

7 / 2         # 3.5   -- true division always returns float
7 // 2        # 3     -- floor division
-7 // 2       # -4    -- floors toward negative infinity, not toward zero
7 % 2         # 1
```

## Type hints do not enforce anything at runtime

```python
def add(a: int, b: int) -> int:
    return a + b

add("x", "y")  # runs fine at runtime -- returns "xy"; only a type
               # checker like mypy would flag this as an error
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| `int("3.5")` | `ValueError` | `int(float("3.5"))` if truncation is intended |
| `-7 // 2` expecting `-3` | Floors toward `-inf`, gives `-4` | Use `int(-7 / 2)` for truncation toward zero |
| Assuming type hints are enforced | Silent wrong-type bugs at runtime | Run `mypy`/`pyright` in CI; hints alone don't check anything |
| `0.1 + 0.2 == 0.3` | `False` -- binary float imprecision | Use `math.isclose()` or `decimal.Decimal` for exact values |
| Confusing `is` with type equality | `type(x) is int` misses `bool`/subclasses | Use `isinstance()` unless you specifically need the exact type |

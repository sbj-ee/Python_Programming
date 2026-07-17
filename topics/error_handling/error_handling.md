# Error Handling

Exceptions are the primary and idiomatic error-handling mechanism in
Python — there is no separate error-code convention. "It's easier to ask
forgiveness than permission" (EAFP) is the prevailing style: try the
operation, handle the exception, rather than checking preconditions first.

## try/except/else/finally

```python
try:
    result = risky_operation()
except ValueError as e:
    print(f"bad value: {e}")
except (TypeError, KeyError) as e:
    print(f"one of two types: {e}")
else:
    print(f"succeeded: {result}")   # runs ONLY if no exception was raised
finally:
    cleanup()                        # ALWAYS runs, exception or not
```

`else` keeps the success path out of the `try` block, so a bug in the
success-handling code isn't accidentally caught by the same `except`.

## Custom exception hierarchies

```python
class ValidationError(Exception):
    """Base class -- callers can catch broadly or narrowly."""

class MissingFieldError(ValidationError):
    def __init__(self, field):
        self.field = field
        super().__init__(f"missing required field: {field}")

class OutOfRangeError(ValidationError):
    pass

try:
    validate(data)
except MissingFieldError as e:
    handle_missing(e.field)
except ValidationError as e:
    handle_generic(e)         # catches any OTHER ValidationError subclass
```

## Exception chaining: raise ... from

```python
def parse_config(raw):
    try:
        return int(raw)
    except ValueError as e:
        raise ValidationError(f"invalid config: {raw!r}") from e
        # preserves the original exception as __cause__, so tracebacks show
        # BOTH "here's what actually broke" and "here's why we re-raised"
```

## EAFP vs LBYL

```python
# LBYL (Look Before You Leap) -- check first, then act
if key in d:
    value = d[key]

# EAFP (Easier to Ask Forgiveness than Permission) -- the Pythonic default
try:
    value = d[key]
except KeyError:
    value = default

# EAFP avoids a race condition (the check and the use are not atomic)
# and is often faster in the common case where the exception is rare.
```

## Exception groups (Python 3.11+)

```python
try:
    raise ExceptionGroup("validation failed", [
        MissingFieldError("name"),
        OutOfRangeError("age out of range"),
    ])
except* MissingFieldError as eg:
    handle_missing_fields(eg.exceptions)
except* OutOfRangeError as eg:
    handle_range_errors(eg.exceptions)
# except* handles MULTIPLE independent exceptions raised together --
# useful for asyncio.TaskGroup, where several concurrent tasks can each fail.
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Bare `except:` | Catches `KeyboardInterrupt`/`SystemExit` too, hides real bugs | `except Exception:` at minimum, or a specific type |
| Catching an exception without re-raising or logging | Silent failure -- the bug disappears without a trace | At minimum, log it; consider `raise` to propagate |
| `except Exception as e: raise ValueError(str(e))` | Loses the original traceback | `raise ValueError(...) from e` |
| Using exceptions for expected, high-frequency control flow | Slower than a plain `if` check in a hot loop | Reserve exceptions for genuinely exceptional conditions |
| Wide `except` blocks that swallow unrelated errors | A `NameError` from a typo gets treated the same as an expected failure | Catch the narrowest exception type that's actually expected |

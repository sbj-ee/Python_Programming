"""Exercise 16: Exceptions.

try/except/else/finally, custom exception hierarchies, exception chaining
with `raise ... from`, and exception groups (Python 3.11+).
"""


class ValidationError(Exception):
    """Base class for this module's errors — lets callers catch broadly
    with `except ValidationError` or narrowly with a specific subclass.
    """


class MissingFieldError(ValidationError):
    def __init__(self, field: str) -> None:
        self.field = field
        super().__init__(f"missing required field: {field}")


class OutOfRangeError(ValidationError):
    def __init__(self, field: str, value: float, low: float, high: float) -> None:
        self.field = field
        super().__init__(f"{field}={value} not in [{low}, {high}]")


def validate_age(data: dict) -> int:
    if "age" not in data:
        raise MissingFieldError("age")
    age = data["age"]
    if not (0 <= age <= 150):
        raise OutOfRangeError("age", age, 0, 150)
    return age


def parse_config_value(raw: str) -> int:
    try:
        return int(raw)
    except ValueError as e:
        # `raise ... from e` preserves the original traceback as the cause,
        # so debugging shows both "what went wrong" and "why we're raising".
        raise ValidationError(f"invalid config value: {raw!r}") from e


def main() -> None:
    # --- try/except/else/finally ---
    for payload in [{"age": 30}, {"age": 200}, {}]:
        try:
            age = validate_age(payload)
        except MissingFieldError as e:
            print(f"missing field: {e}")
        except OutOfRangeError as e:
            print(f"out of range: {e}")
        except ValidationError as e:
            # Catches any other ValidationError subclass not handled above.
            print(f"validation failed: {e}")
        else:
            # Runs only if no exception was raised — keeps the success path
            # out of the try block, so it isn't accidentally caught too.
            print(f"valid age: {age}")
        finally:
            # Always runs, exception or not — the place for cleanup.
            print(f"  (checked payload: {payload})")

    # --- Exception chaining ---
    try:
        parse_config_value("not-a-number")
    except ValidationError as e:
        print(f"chained error: {e}")
        print(f"  __cause__: {e.__cause__!r}")

    # --- Catching multiple exception types in one clause ---
    for value in ["42", "oops", None]:
        try:
            result = int(value)  # type: ignore[arg-type]
        except (TypeError, ValueError) as e:
            print(f"{value!r} -> error: {type(e).__name__}: {e}")
        else:
            print(f"{value!r} -> {result}")

    # --- Exception groups (3.11+): raise/handle multiple errors at once ---
    try:
        raise ExceptionGroup(
            "validation failed",
            [MissingFieldError("name"), OutOfRangeError("age", -1, 0, 150)],
        )
    except* MissingFieldError as eg:
        print(f"missing fields: {[str(e) for e in eg.exceptions]}")
    except* OutOfRangeError as eg:
        print(f"out of range fields: {[str(e) for e in eg.exceptions]}")


if __name__ == "__main__":
    main()

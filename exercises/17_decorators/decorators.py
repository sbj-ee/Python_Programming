"""Exercise 17: Decorators.

A decorator is a function that takes a function and returns a (usually
wrapped) function. The `@decorator` syntax is sugar for `func = decorator(func)`.
"""

import functools
import time


def timer(func):
    """A basic decorator: wraps `func`, timing each call."""

    @functools.wraps(func)  # preserves func.__name__, __doc__, etc.
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"  {func.__name__} took {elapsed * 1000:.3f}ms")
        return result

    return wrapper


def retry(times: int):
    """A decorator FACTORY: a function that returns a decorator, letting
    the decorator itself take arguments via the @retry(times=3) syntax.
    """

    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            last_exc = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as e:
                    last_exc = e
                    print(f"  attempt {attempt} failed: {e}")
            raise last_exc

        return wrapper

    return decorator


def log_calls(cls):
    """Class decorators work the same way — take a class, return a class."""
    original_init = cls.__init__

    def new_init(self, *args, **kwargs):
        print(f"  constructing {cls.__name__}({args}, {kwargs})")
        original_init(self, *args, **kwargs)

    cls.__init__ = new_init
    return cls


@timer
def slow_add(a: int, b: int) -> int:
    time.sleep(0.01)
    return a + b


_flaky_attempts = 0


@retry(times=3)
def flaky_operation() -> str:
    global _flaky_attempts
    _flaky_attempts += 1
    if _flaky_attempts < 3:
        raise ValueError(f"transient failure #{_flaky_attempts}")
    return "success"


@log_calls
class Widget:
    def __init__(self, name: str) -> None:
        self.name = name


def main() -> None:
    print(f"slow_add(2, 3) = {slow_add(2, 3)}")
    print(f"slow_add.__name__ = {slow_add.__name__}  (preserved by functools.wraps)")

    print(f"flaky_operation() = {flaky_operation()}")

    Widget("gadget")

    # --- Stacking decorators: applied bottom-up, unwound top-down ---
    @timer
    @retry(times=2)
    def combined() -> str:
        return "ok"

    print(f"combined() = {combined()}")

    # --- A decorator without @functools.wraps loses introspection info ---
    def naive_decorator(func):
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)

        return wrapper

    @naive_decorator
    def example():
        """Original docstring."""

    print(f"naive-decorated __name__: {example.__name__}  (lost, now 'wrapper')")


if __name__ == "__main__":
    main()

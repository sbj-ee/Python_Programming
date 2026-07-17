"""Exercise 04: Functions.

def, positional/keyword/default arguments, *args/**kwargs, docstrings,
and recursion.
"""

from collections.abc import Callable


def greet(name: str, greeting: str = "Hello") -> str:
    """Return a greeting. `greeting` has a default, so callers may omit it."""
    return f"{greeting}, {name}!"


def describe(*args: int, **kwargs: str) -> None:
    """`*args` collects extra positional arguments into a tuple.

    `**kwargs` collects extra keyword arguments into a dict.
    """
    print(f"positional args: {args}")
    print(f"keyword args: {kwargs}")


def summarize(a: int, b: int, /, c: int, *, d: int) -> int:
    """`/` marks the end of positional-only parameters; `*` marks the start
    of keyword-only parameters. `a, b` must be positional; `d` must be named.
    """
    return a + b + c + d


def factorial(n: int) -> int:
    """Recursion: a function that calls itself on a smaller subproblem."""
    if n <= 1:
        return 1
    return n * factorial(n - 1)


def make_counter() -> Callable[[], int]:
    """Functions are first-class values: this returns a function."""
    count = 0

    def increment() -> int:
        nonlocal count  # without this, `count += 1` below would raise
        count += 1  # UnboundLocalError (assignment creates a new local)
        return count

    return increment


def main() -> None:
    print(greet("Ada"))
    print(greet("Linus", greeting="Hi"))

    describe(1, 2, 3, x="a", y="b")

    print(f"summarize(1, 2, c=3, d=4) = {summarize(1, 2, c=3, d=4)}")
    # summarize(a=1, b=2, c=3, d=4) would raise TypeError: a, b are positional-only

    print(f"factorial(5) = {factorial(5)}")

    counter = make_counter()
    print(f"counter() = {counter()}")
    print(f"counter() = {counter()}")
    print(f"counter() = {counter()}")

    # --- Unpacking arguments with * and ** ---
    numbers = [10, 20, 30]
    print("describe(*numbers) unpacks the list as positional args:")
    describe(*numbers)

    options = {"mode": "fast", "level": "high"}
    print("describe(**options) unpacks the dict as keyword args:")
    describe(**options)


if __name__ == "__main__":
    main()

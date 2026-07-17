"""Exercise 11: Closures & Higher-Order Functions.

Functions are first-class objects: they can be passed as arguments, returned
from other functions, and stored in data structures. A closure is a function
that remembers the variables from the scope it was defined in.
"""

from functools import reduce


def make_multiplier(factor: int):
    """Returns a function that closes over `factor`."""

    def multiplier(x: int) -> int:
        return x * factor

    return multiplier


def make_accumulator():
    """Each call to the returned function updates state private to this
    closure — no class needed for simple stateful behavior.
    """
    total = 0

    def add(amount: int) -> int:
        nonlocal total
        total += amount
        return total

    return add


def apply_twice(func, value):
    """A higher-order function: takes a function as an argument."""
    return func(func(value))


def main() -> None:
    double = make_multiplier(2)
    triple = make_multiplier(3)
    print(f"double(5) = {double(5)}")
    print(f"triple(5) = {triple(5)}")

    acc = make_accumulator()
    print(f"acc(10) = {acc(10)}")
    print(f"acc(5) = {acc(5)}")
    print(f"acc(-3) = {acc(-3)}")

    # --- Higher-order functions: map, filter, reduce ---
    numbers = [1, 2, 3, 4, 5, 6, 7, 8]
    squared = list(map(lambda x: x * x, numbers))
    evens = list(filter(lambda x: x % 2 == 0, numbers))
    total = reduce(lambda acc, x: acc + x, numbers, 0)

    print(f"squared = {squared}")
    print(f"evens = {evens}")
    print(f"total (via reduce) = {total}")

    # --- Idiomatic Python usually prefers comprehensions to map/filter ---
    squared_comp = [x * x for x in numbers]
    evens_comp = [x for x in numbers if x % 2 == 0]
    print(f"squared_comp == squared: {squared_comp == squared}")
    print(f"evens_comp == evens: {evens_comp == evens}")

    print(f"apply_twice(double, 3) = {apply_twice(double, 3)}")

    # --- Functions stored in a dict act as a dispatch table ---
    ops = {
        "add": lambda a, b: a + b,
        "sub": lambda a, b: a - b,
        "mul": lambda a, b: a * b,
    }
    for name, op in ops.items():
        print(f"ops['{name}'](6, 3) = {op(6, 3)}")

    # --- sorted() takes a key function: a higher-order function in daily use ---
    words = ["banana", "kiwi", "apple", "fig"]
    by_length = sorted(words, key=len)
    print(f"sorted by length: {by_length}")


if __name__ == "__main__":
    main()

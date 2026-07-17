"""Exercise 18: Generators & Iterators.

The iterator protocol (__iter__/__next__), generator functions (yield), and
generator expressions — Python's lazy, memory-efficient alternative to
building an entire collection up front.
"""

import itertools


class CountUp:
    """A hand-rolled iterator implementing the iterator protocol directly."""

    def __init__(self, start: int, stop: int) -> None:
        self.current = start
        self.stop = stop

    def __iter__(self) -> "CountUp":
        return self  # an iterator is its own iterable

    def __next__(self) -> int:
        if self.current >= self.stop:
            raise StopIteration
        value = self.current
        self.current += 1
        return value


def count_up_gen(start: int, stop: int):
    """The same behavior as CountUp, but `yield` writes the iterator for
    you. Each call generates one value and suspends until asked for the next.
    """
    current = start
    while current < stop:
        yield current
        current += 1


def fibonacci():
    """An infinite generator — only safe because consumers control how
    many values they pull (e.g. with itertools.islice or a break).
    """
    a, b = 0, 1
    while True:
        yield a
        a, b = b, a + b


def read_large_file_lines(lines: list[str]):
    """A generator pipeline: each stage processes one item at a time
    instead of materializing an intermediate list — the pattern that
    matters for genuinely large files.
    """
    stripped = (line.strip() for line in lines)
    non_empty = (line for line in stripped if line)
    yield from non_empty


def main() -> None:
    print("CountUp (hand-rolled iterator):", list(CountUp(0, 5)))
    print("count_up_gen (generator function):", list(count_up_gen(0, 5)))

    # --- Generators are lazy: nothing runs until you iterate ---
    gen = count_up_gen(0, 3)
    print(f"gen object: {gen}  (no values computed yet)")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    print(f"next(gen) = {next(gen)}")
    try:
        next(gen)
    except StopIteration:
        print("exhausted: StopIteration raised")

    # --- Infinite generator, safely bounded by the consumer ---
    first_ten_fib = list(itertools.islice(fibonacci(), 10))
    print(f"first 10 Fibonacci numbers: {first_ten_fib}")

    # --- Generator expression: like a list comprehension, but lazy ---
    squares_gen = (x * x for x in range(1_000_000))  # no memory allocated yet
    print(f"first 5 squares via itertools.islice: {list(itertools.islice(squares_gen, 5))}")

    raw_lines = ["  hello  ", "", "world", "   ", "python"]
    print(f"cleaned lines: {list(read_large_file_lines(raw_lines))}")

    # --- itertools: the standard toolbox for iterator composition ---
    print(f"itertools.chain: {list(itertools.chain([1, 2], [3, 4]))}")
    print(f"itertools.combinations: {list(itertools.combinations('ABC', 2))}")
    print(f"itertools.groupby: {[(k, list(g)) for k, g in itertools.groupby('aaabbc')]}")


if __name__ == "__main__":
    main()

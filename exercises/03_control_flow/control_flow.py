"""Exercise 03: Control Flow.

if/elif/else, while, for, structural pattern matching (match, Python 3.10+),
and comprehensions as a fourth kind of "loop" for building collections.
"""


def classify(n: int) -> str:
    if n < 0:
        return "negative"
    elif n == 0:
        return "zero"
    else:
        return "positive"


def match_shape(shape: object) -> str:
    # `match` compares structure, not just value. Tuples, dicts, and classes
    # can all be destructured directly in the pattern.
    match shape:
        case ("circle", radius) if radius > 0:  # type: ignore[operator]
            return f"circle with radius {radius}"
        case ("rectangle", width, height):
            return f"rectangle {width}x{height}"
        case ["point", *rest] if rest:
            return f"point with extra data: {rest}"
        case str() as s:
            return f"just a string: {s}"
        case _:
            return "unknown shape"


def main() -> None:
    for n in (-3, 0, 7):
        print(f"classify({n}) = {classify(n)}")

    # --- while loop with break/continue ---
    total, i = 0, 0
    while i < 10:
        i += 1
        if i % 2 == 0:
            continue  # skip even numbers
        if i > 7:
            break
        total += i
    print(f"sum of odd numbers up to 7 = {total}")

    # --- for loop over a range and over a collection ---
    for i in range(3):
        print(f"range item {i}")
    for word in ["fast", "clear", "correct"]:
        print(f"word: {word}")

    # --- for/else: else runs only if the loop was NOT broken out of ---
    for n in range(2, 10):
        if n % 7 == 0:
            print(f"found a multiple of 7: {n}")
            break
    else:
        print("no multiple of 7 found")

    # --- match statement ---
    for shape in (("circle", 2.0), ("rectangle", 3, 4), ["point", 1, 2], "hi", 42):
        print(f"match_shape({shape!r}) = {match_shape(shape)}")

    # --- comprehensions: build a collection in one expression ---
    squares = [x * x for x in range(6)]
    evens_only = [x for x in range(20) if x % 2 == 0]
    lookup = {x: x * x for x in range(5)}
    unique_lengths = {len(w) for w in ["a", "bb", "cc", "ddd"]}

    print(f"squares = {squares}")
    print(f"evens_only = {evens_only}")
    print(f"lookup = {lookup}")
    print(f"unique_lengths = {unique_lengths}")


if __name__ == "__main__":
    main()

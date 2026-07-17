"""Exercise 02: Variables & Types.

Python is dynamically typed: a name is bound to a value, and that value
carries its own type. The name itself has no declared type and can be
rebound to a value of a different type at any time.
"""


def main() -> None:
    # --- Core built-in types ---
    count: int = 42
    ratio: float = 3.14159
    name: str = "Ada"
    is_active: bool = True
    nothing = None

    print(f"{count=} {type(count).__name__}")
    print(f"{ratio=} {type(ratio).__name__}")
    print(f"{name=} {type(name).__name__}")
    print(f"{is_active=} {type(is_active).__name__}")
    print(f"{nothing=} {type(nothing).__name__}")

    # --- Dynamic typing: the name can be rebound to any type ---
    thing = 10
    print(f"thing is {thing!r} ({type(thing).__name__})")
    thing = "now a string"  # type: ignore[assignment]  # dynamic typing, deliberately shown
    print(f"thing is {thing!r} ({type(thing).__name__})")

    # --- int has arbitrary precision; no overflow ---
    big = 2**100
    print(f"2**100 = {big}")

    # --- Integer division vs. float division ---
    print(f"7 / 2 = {7 / 2}")   # true division -> float
    print(f"7 // 2 = {7 // 2}")  # floor division -> int
    print(f"7 % 2 = {7 % 2}")    # modulo

    # --- bool is a subclass of int ---
    print(f"isinstance(True, int) = {isinstance(True, int)}")
    print(f"True + True = {True + True}")

    # --- Explicit casting ---
    print(f"int('42') = {int('42')}")
    print(f"float('3.5') = {float('3.5')}")
    print(f"str(99) = {str(99)!r}")
    print(f"bool(0) = {bool(0)}, bool('') = {bool('')}, bool([1]) = {bool([1])}")

    # --- type() vs isinstance(): isinstance respects subclassing ---
    print(f"type(is_active) is bool: {type(is_active) is bool}")
    print(f"isinstance(is_active, int): {isinstance(is_active, int)}")


if __name__ == "__main__":
    main()

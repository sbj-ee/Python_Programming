"""Exercise 13: Operator Overloading.

Dunder ("double underscore") methods let user-defined classes respond to
built-in operators, printing, and hashing the same way built-in types do.
"""

from __future__ import annotations


class Vector2:
    """A 2D vector with arithmetic operators, equality, and a hash."""

    def __init__(self, x: float, y: float) -> None:
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        # Unambiguous, developer-facing representation.
        return f"Vector2({self.x}, {self.y})"

    def __str__(self) -> str:
        # Friendlier, user-facing representation; falls back to __repr__
        # if not defined. print() uses __str__.
        return f"({self.x}, {self.y})"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Vector2):
            return NotImplemented
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        # Defining __eq__ disables the default __hash__; redefine it
        # explicitly if instances need to go in a set or dict key.
        return hash((self.x, self.y))

    def __add__(self, other: Vector2) -> Vector2:
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: Vector2) -> Vector2:
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> Vector2:
        return Vector2(self.x * scalar, self.y * scalar)

    def __rmul__(self, scalar: float) -> Vector2:
        # Enables `scalar * vector` (Python tries __mul__ on the left
        # operand first; when that's NotImplemented or absent for the type,
        # it falls back to __rmul__ on the right operand).
        return self.__mul__(scalar)

    def __neg__(self) -> Vector2:
        return Vector2(-self.x, -self.y)

    def __abs__(self) -> float:
        return (self.x**2 + self.y**2) ** 0.5

    def __lt__(self, other: Vector2) -> bool:
        return abs(self) < abs(other)


class Inventory:
    """Demonstrates __len__, __getitem__, and __contains__."""

    def __init__(self) -> None:
        self._items: dict[str, int] = {}

    def __len__(self) -> int:
        return len(self._items)

    def __getitem__(self, key: str) -> int:
        return self._items[key]

    def __setitem__(self, key: str, value: int) -> None:
        self._items[key] = value

    def __contains__(self, key: str) -> bool:
        return key in self._items


def main() -> None:
    v1 = Vector2(1, 2)
    v2 = Vector2(3, 4)

    print(f"v1 = {v1}, repr(v1) = {v1!r}")
    print(f"v1 + v2 = {v1 + v2}")
    print(f"v1 - v2 = {v1 - v2}")
    print(f"v1 * 3 = {v1 * 3}")
    print(f"3 * v1 = {3 * v1}")  # uses __rmul__
    print(f"-v1 = {-v1}")
    print(f"abs(v2) = {abs(v2)}")
    print(f"v1 == Vector2(1, 2): {v1 == Vector2(1, 2)}")
    print(f"v1 < v2: {v1 < v2}")

    vectors = sorted([v2, v1, Vector2(0, 0)])
    print(f"sorted by magnitude: {vectors}")

    seen = {v1, Vector2(1, 2)}  # equal + same hash -> one entry
    print(f"deduplicated set size: {len(seen)}")

    inv = Inventory()
    inv["apples"] = 10
    inv["pears"] = 4
    print(f"len(inv) = {len(inv)}")
    print(f"inv['apples'] = {inv['apples']}")
    print(f"'pears' in inv: {'pears' in inv}")
    print(f"'kiwi' in inv: {'kiwi' in inv}")


if __name__ == "__main__":
    main()

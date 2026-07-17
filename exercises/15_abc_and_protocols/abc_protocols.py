"""Exercise 15: ABCs & Protocols.

abc.ABC enforces a nominal contract: subclasses MUST implement abstract
methods, checked at instantiation time. typing.Protocol enforces a
structural contract: any object with the right shape satisfies it, with
no inheritance required (Python's version of duck typing, made explicit).
"""

from abc import ABC, abstractmethod
from typing import Protocol, runtime_checkable


class Shape(ABC):
    """Nominal typing: you must subclass Shape and implement `area`."""

    @abstractmethod
    def area(self) -> float: ...

    def describe(self) -> str:
        # Concrete methods are allowed alongside abstract ones.
        return f"{type(self).__name__} with area {self.area():.2f}"


class Circle(Shape):
    def __init__(self, radius: float) -> None:
        self.radius = radius

    def area(self) -> float:
        return 3.14159265 * self.radius**2


class Square(Shape):
    def __init__(self, side: float) -> None:
        self.side = side

    def area(self) -> float:
        return self.side**2


@runtime_checkable
class HasArea(Protocol):
    """Structural typing: ANY object with an `area()` method matches,
    whether or not it inherits from anything in particular.
    """

    def area(self) -> float: ...


class UnrelatedRectangle:
    """Does not inherit from Shape or HasArea, yet still satisfies HasArea."""

    def __init__(self, width: float, height: float) -> None:
        self.width = width
        self.height = height

    def area(self) -> float:
        return self.width * self.height


def total_area(shapes: list[HasArea]) -> float:
    """Accepts anything structurally shaped like HasArea — Shape subclasses
    and UnrelatedRectangle alike.
    """
    return sum(s.area() for s in shapes)


def main() -> None:
    try:
        Shape()  # type: ignore[abstract]
    except TypeError as e:
        print(f"cannot instantiate ABC directly: {e}")

    shapes: list[Shape] = [Circle(2.0), Square(3.0)]
    for s in shapes:
        print(s.describe())

    # --- Structural typing in action ---
    rect = UnrelatedRectangle(4.0, 5.0)
    print(f"isinstance(rect, HasArea): {isinstance(rect, HasArea)}")
    print(f"isinstance(rect, Shape): {isinstance(rect, Shape)}")

    mixed: list[HasArea] = [*shapes, rect]
    print(f"total_area(mixed) = {total_area(mixed):.2f}")


if __name__ == "__main__":
    main()

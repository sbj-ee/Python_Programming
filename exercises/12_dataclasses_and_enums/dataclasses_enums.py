"""Exercise 12: Dataclasses & Enums.

@dataclass generates __init__, __repr__, and __eq__ from type-annotated
class attributes. Enum gives named, type-safe constants; NamedTuple gives
lightweight immutable records.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import NamedTuple


class Status(Enum):
    """Plain Enum: distinct, comparable, named members."""

    PENDING = auto()
    ACTIVE = auto()
    DONE = auto()

    def __str__(self) -> str:
        return self.name.title()


@dataclass
class Task:
    title: str
    status: Status = Status.PENDING
    tags: list[str] = field(default_factory=list)  # mutable default, done safely

    def mark_done(self) -> None:
        self.status = Status.DONE


@dataclass(frozen=True)
class Point:
    """frozen=True makes instances immutable and hashable."""

    x: float
    y: float

    def distance_to(self, other: "Point") -> float:
        return ((self.x - other.x) ** 2 + (self.y - other.y) ** 2) ** 0.5


class Color(NamedTuple):
    """NamedTuple: an immutable, indexable, unpackable record."""

    red: int
    green: int
    blue: int


def main() -> None:
    # --- Enum ---
    print(f"Status.ACTIVE = {Status.ACTIVE}")
    print(f"Status.ACTIVE.value = {Status.ACTIVE.value}")
    print(f"Status.ACTIVE == Status.ACTIVE: {Status.ACTIVE == Status.ACTIVE}")
    print(f"Status.ACTIVE == Status.DONE: {Status.ACTIVE == Status.DONE}")
    for status in Status:
        print(f"  {status.name} = {status.value}")

    # --- dataclass: __init__/__repr__/__eq__ generated for free ---
    t1 = Task(title="Write exercise 12", tags=["python", "learning"])
    t2 = Task(title="Write exercise 12", tags=["python", "learning"])
    print(f"t1 = {t1}")
    print(f"t1 == t2 (value equality): {t1 == t2}")
    t1.mark_done()
    print(f"after mark_done: {t1}")

    # --- frozen dataclass: immutable, safe to hash and use as a dict key ---
    p1 = Point(0.0, 0.0)
    p2 = Point(3.0, 4.0)
    print(f"distance p1->p2 = {p1.distance_to(p2)}")
    try:
        p1.x = 99.0  # type: ignore[misc]
    except AttributeError as e:
        print(f"cannot mutate frozen dataclass: {e}")

    points_seen = {p1, p2}  # hashable because frozen=True
    print(f"points_seen has 2 entries: {len(points_seen) == 2}")

    # --- NamedTuple: tuple-like, but with named field access ---
    red = Color(255, 0, 0)
    print(f"red = {red}, red.red = {red.red}, red[0] = {red[0]}")
    r, g, b = red  # unpacks like a plain tuple
    print(f"unpacked: r={r} g={g} b={b}")


if __name__ == "__main__":
    main()

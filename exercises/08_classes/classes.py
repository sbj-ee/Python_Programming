"""Exercise 08: Classes.

class, __init__, instance attributes vs. class attributes, methods,
and the difference between the two kinds of attribute.
"""


class Counter:
    """A simple counter demonstrating instance state and class-level state."""

    # Class attribute: shared by every instance unless shadowed by an
    # instance attribute of the same name.
    total_created = 0

    def __init__(self, start: int = 0) -> None:
        # Instance attributes: unique to each object, set on `self`.
        self.value = start
        Counter.total_created += 1  # mutate the class attribute explicitly

    def increment(self, by: int = 1) -> None:
        self.value += by

    def reset(self) -> None:
        self.value = 0

    def __repr__(self) -> str:
        # __repr__ controls how the object prints in debuggers, REPLs, and
        # inside containers like lists. Aim for something that could
        # recreate the object.
        return f"Counter(value={self.value})"


class Student:
    """Demonstrates a typical multi-attribute class with a computed method."""

    def __init__(self, name: str, grades: list[float]) -> None:
        self.name = name
        self.grades = grades

    def average(self) -> float:
        if not self.grades:
            return 0.0
        return sum(self.grades) / len(self.grades)

    def add_grade(self, grade: float) -> None:
        self.grades.append(grade)


def main() -> None:
    c1 = Counter()
    c2 = Counter(start=10)

    c1.increment()
    c1.increment(by=5)
    c2.increment(by=-1)

    print(f"c1 = {c1}")
    print(f"c2 = {c2}")
    print(f"Counter.total_created = {Counter.total_created}")

    c1.reset()
    print(f"after reset, c1 = {c1}")

    # --- Instance attribute shadows class attribute of the same name ---
    c1.total_created = "shadowed!"  # type: ignore[assignment]  # creates an INSTANCE attribute
    print(f"c1.total_created = {c1.total_created}  (instance-level now)")
    print(f"Counter.total_created = {Counter.total_created}  (class unaffected)")

    student = Student("Ada", [88.0, 92.5, 79.0])
    print(f"{student.name}'s average: {student.average():.2f}")
    student.add_grade(95.0)
    print(f"after adding a grade: {student.average():.2f}")


if __name__ == "__main__":
    main()

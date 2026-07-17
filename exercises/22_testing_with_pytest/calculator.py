"""The module under test for Exercise 22."""


class DivisionByZeroError(Exception):
    pass


class Calculator:
    def __init__(self) -> None:
        self.history: list[str] = []

    def add(self, a: float, b: float) -> float:
        result = a + b
        self.history.append(f"{a} + {b} = {result}")
        return result

    def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise DivisionByZeroError("cannot divide by zero")
        result = a / b
        self.history.append(f"{a} / {b} = {result}")
        return result


def is_prime(n: int) -> bool:
    if n < 2:
        return False
    for divisor in range(2, int(n**0.5) + 1):
        if n % divisor == 0:
            return False
    return True

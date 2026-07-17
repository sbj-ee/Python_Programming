"""Exercise 22: Testing with pytest.

Run with `pytest exercises/22_testing_with_pytest` or `uv run pytest`.
Demonstrates plain assert-based tests, fixtures, parametrize, exception
testing, and monkeypatch.
"""

import pytest
from calculator import Calculator, DivisionByZeroError, is_prime


# --- A fixture provides fresh, isolated setup to every test that requests it ---
@pytest.fixture
def calc() -> Calculator:
    return Calculator()


def test_add(calc: Calculator) -> None:
    assert calc.add(2, 3) == 5


def test_add_records_history(calc: Calculator) -> None:
    calc.add(1, 1)
    calc.add(2, 2)
    assert calc.history == ["1 + 1 = 2", "2 + 2 = 4"]


def test_divide(calc: Calculator) -> None:
    assert calc.divide(10, 2) == 5


def test_divide_by_zero_raises(calc: Calculator) -> None:
    # pytest.raises both asserts the exception type AND lets you inspect it.
    with pytest.raises(DivisionByZeroError, match="cannot divide by zero"):
        calc.divide(1, 0)


# --- parametrize runs the same test body against a table of inputs ---
@pytest.mark.parametrize(
    "n,expected",
    [
        (1, False),
        (2, True),
        (3, True),
        (4, False),
        (17, True),
        (18, False),
    ],
)
def test_is_prime(n: int, expected: bool) -> None:
    assert is_prime(n) == expected


class TestCalculatorHistory:
    """Grouping related tests in a class is optional in pytest, but useful
    for sharing fixtures via setup methods or class-scoped fixtures.
    """

    def test_empty_history_on_creation(self, calc: Calculator) -> None:
        assert calc.history == []

    def test_history_accumulates_across_operations(self, calc: Calculator) -> None:
        calc.add(1, 2)
        calc.divide(10, 5)
        assert len(calc.history) == 2


def test_monkeypatch_environment(monkeypatch: pytest.MonkeyPatch) -> None:
    """monkeypatch safely sets/restores state (env vars, attributes) for
    the duration of a single test, undoing the change automatically after.
    """
    import os

    monkeypatch.setenv("CALCULATOR_MODE", "scientific")
    assert os.environ["CALCULATOR_MODE"] == "scientific"
    # No manual cleanup needed — pytest reverts this after the test.

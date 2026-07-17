"""A sibling module inside the package."""


def add(a: int, b: int) -> int:
    return a + b


def multiply(a: int, b: int) -> int:
    return a * b


def _internal_only() -> str:
    """Leading underscore signals 'not part of the public API' — a
    convention, not an enforced boundary. It is still importable.
    """
    return "not meant to be used outside this module"

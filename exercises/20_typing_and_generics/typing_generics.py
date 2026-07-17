"""Exercise 20: Typing & Generics.

Type hints are optional and unenforced at runtime — Python remains dynamically
typed. Tools like mypy read the hints statically and catch mismatches before
the code ever runs. This file is intentionally 100% mypy-clean; run
`uv run mypy exercises/20_typing_and_generics` to see it pass.
"""

from typing import Generic, Optional, TypeVar, Union

T = TypeVar("T")


def first_or_default(items: list[T], default: T) -> T:
    """Generic function: works for any T, and mypy tracks that the return
    type matches whatever T was inferred from the call site.
    """
    return items[0] if items else default


class Stack(Generic[T]):
    """A generic class: Stack[int] and Stack[str] are distinct, checked
    types to a static analyzer, while sharing one implementation at runtime.
    """

    def __init__(self) -> None:
        self._items: list[T] = []

    def push(self, item: T) -> None:
        self._items.append(item)

    def pop(self) -> T:
        return self._items.pop()

    def peek(self) -> Optional[T]:
        return self._items[-1] if self._items else None

    def __len__(self) -> int:
        return len(self._items)


def describe_value(value: Union[int, str, None]) -> str:
    """Union types: the parameter may be one of several types. `None` in a
    Union is the idiomatic way to express "optional" (Optional[X] is
    shorthand for Union[X, None]).
    """
    if value is None:
        return "nothing"
    if isinstance(value, int):
        return f"an integer: {value}"
    return f"a string: {value!r}"


def safe_divide(a: float, b: float) -> Optional[float]:
    if b == 0:
        return None
    return a / b


def main() -> None:
    print(f"first_or_default([1,2,3], 0) = {first_or_default([1, 2, 3], 0)}")
    print(f"first_or_default([], 'none') = {first_or_default([], 'none')}")

    int_stack: Stack[int] = Stack()
    int_stack.push(1)
    int_stack.push(2)
    print(f"int_stack.peek() = {int_stack.peek()}")
    print(f"int_stack.pop() = {int_stack.pop()}")
    print(f"len(int_stack) = {len(int_stack)}")

    str_stack: Stack[str] = Stack()
    str_stack.push("a")
    str_stack.push("b")
    print(f"str_stack.pop() = {str_stack.pop()}")

    for v in (42, "hello", None):
        print(f"describe_value({v!r}) = {describe_value(v)}")

    for a, b in [(10, 2), (5, 0)]:
        result = safe_divide(a, b)
        # mypy would flag `result + 1` here without this narrowing check —
        # `Optional[float]` must be proven non-None before arithmetic.
        if result is not None:
            print(f"{a}/{b} = {result}")
        else:
            print(f"{a}/{b} = undefined (division by zero)")


if __name__ == "__main__":
    main()

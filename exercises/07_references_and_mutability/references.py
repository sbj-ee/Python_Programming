"""Exercise 07: References & Mutability.

A Python variable is a name bound to an object, not a box holding a value.
Assignment binds a name; it never copies. Understanding this is the single
most important mental model shift for programmers coming from C/C++.
"""

import copy


def append_bad(item: int, target: list[int] = []) -> list[int]:  # noqa: B006
    """The classic pitfall: a mutable default argument is created ONCE,
    at function definition time, and reused across every call that doesn't
    supply its own. Deliberately kept here (with noqa) to demonstrate it.
    """
    target.append(item)
    return target


def append_good(item: int, target: list[int] | None = None) -> list[int]:
    """The fix: default to None, create the mutable object inside the call."""
    if target is None:
        target = []
    target.append(item)
    return target


def main() -> None:
    # --- Names are bindings, not boxes ---
    a = [1, 2, 3]
    b = a  # b now refers to the SAME list object as a
    b.append(4)
    print(f"a = {a}, b = {b}")  # both show the append
    print(f"a is b: {a is b}")
    print(f"id(a) == id(b): {id(a) == id(b)}")

    # --- Reassignment breaks the link; it doesn't mutate the old object ---
    c = a
    c = [9, 9, 9]  # rebinds c to a new list; a is untouched
    print(f"a = {a}, c = {c}")

    # --- is vs == ---
    x = [1, 2]
    y = [1, 2]
    print(f"x == y: {x == y} (same contents)")
    print(f"x is y: {x is y} (different objects)")

    # --- Small ints and interned strings may be cached by CPython ---
    m, n = 5, 5
    print(f"m is n: {m is n} (small ints are cached, -5..256)")

    # --- Function arguments are passed by object reference ---
    def mutate_in_place(lst: list[int]) -> None:
        lst.append(99)  # mutates the caller's list

    def rebind_only(lst: list[int]) -> None:
        lst = [0, 0, 0]  # noqa: F841 -- rebinds the LOCAL name only; caller unaffected

    shared = [1, 2]
    mutate_in_place(shared)
    print(f"after mutate_in_place: {shared}")
    rebind_only(shared)
    print(f"after rebind_only (unchanged): {shared}")

    # --- The mutable default argument trap ---
    print(f"append_bad(1) = {append_bad(1)}")
    print(f"append_bad(2) = {append_bad(2)}  <- leaked state from prior call!")
    print(f"append_good(1) = {append_good(1)}")
    print(f"append_good(2) = {append_good(2)}  <- correctly independent")

    # --- Shallow vs. deep copy ---
    nested = [[1, 2], [3, 4]]
    shallow = copy.copy(nested)
    deep = copy.deepcopy(nested)
    nested[0].append(99)
    print(f"original: {nested}")
    print(f"shallow copy (inner lists shared): {shallow}")
    print(f"deep copy (fully independent): {deep}")


if __name__ == "__main__":
    main()

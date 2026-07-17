"""Exercise 05: Strings & Lists.

str is immutable; list is mutable. Both support slicing with the same
[start:stop:step] syntax.
"""


def main() -> None:
    # --- String basics ---
    s = "  Python Programming  "
    print(f"{s.strip()=}")
    print(f"{s.strip().lower()=}")
    print(f"{s.strip().upper()=}")
    print(f"{s.strip().replace('Python', 'Modern Python')=}")
    print(f"{s.strip().split()=}")
    print(f"{'-'.join(['a', 'b', 'c'])=}")
    print(f"{'Programming'.startswith('Pro')=}")
    print(f"{'Programming'.find('gram')=}")

    # --- f-strings: expressions, format specs, and debugging (=) ---
    name, score = "Grace", 97.456
    print(f"{name} scored {score:.1f}%")
    print(f"{score=:.2f}")
    print(f"{name:>10}|")  # right-align in a 10-char field

    # --- Strings are immutable: methods return new strings ---
    original = "immutable"
    upper = original.upper()
    print(f"original is still {original!r}; upper is {upper!r}")

    # --- Slicing: works identically on str and list ---
    text = "abcdefgh"
    print(f"{text[2:5]=}")
    print(f"{text[:3]=}")
    print(f"{text[-3:]=}")
    print(f"{text[::2]=}")
    print(f"{text[::-1]=}")  # reverse

    # --- Lists: mutable, ordered, heterogeneous ---
    nums = [3, 1, 4, 1, 5, 9, 2, 6]
    nums.append(5)
    nums.sort()
    print(f"sorted nums = {nums}")

    nums.remove(1)  # removes first occurrence
    print(f"after remove(1) = {nums}")

    doubled = [n * 2 for n in nums]
    print(f"doubled = {doubled}")

    # --- Common pitfall: list * n repeats REFERENCES for mutable elements ---
    rows = [[0] * 3 for _ in range(2)]  # correct: independent inner lists
    rows[0][0] = 9
    print(f"independent rows = {rows}")

    wrong_rows = [[0] * 3] * 2  # wrong: same inner list repeated
    wrong_rows[0][0] = 9
    print(f"aliased rows (pitfall) = {wrong_rows}")

    # --- Concatenation and membership ---
    combined = [1, 2] + [3, 4]
    print(f"combined = {combined}")
    print(f"3 in combined = {3 in combined}")


if __name__ == "__main__":
    main()

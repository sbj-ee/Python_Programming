"""Exercise 01: Hello World.

The smallest possible Python program. No compiler, no build step —
`python3 hello.py` reads this file top to bottom and executes it.
"""

# A single-line comment starts with '#'. There is no block-comment syntax;
# consecutive '#' lines or a triple-quoted string (like the docstring above)
# serve that purpose.


def main() -> None:
    print("Hello, World!")

    # print() accepts multiple arguments, joined by `sep` (default a space),
    # and ends with `end` (default a newline).
    print("Hello", "again", sep=", ", end="!\n")

    # Everything after '#' to end of line is ignored by the interpreter.
    print("This line runs.")  # this comment does not


# `__name__` is "__main__" only when this file is run directly, not when it
# is imported by another module. This guard is idiomatic in every exercise
# from here on — it lets a file be both a runnable script and an importable
# module without the demo code firing on import.
if __name__ == "__main__":
    main()

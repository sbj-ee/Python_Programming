"""Exercise 21: Modules & Packages.

A module is any .py file; a package is a directory containing __init__.py
plus modules. This script imports from the sibling `mypackage/` package
three different ways to show how each affects the importing namespace.
"""

import mypackage  # runs mypackage/__init__.py once, caches it in sys.modules
import mypackage.helpers as helpers  # explicit submodule import
from mypackage import add  # names re-exported by __init__.py
from mypackage.helpers import multiply  # reach directly into a submodule


def main() -> None:
    # --- Every import style ends up calling the same underlying function ---
    print(f"mypackage.add(2, 3) = {mypackage.add(2, 3)}")
    print(f"helpers.add(2, 3) = {helpers.add(2, 3)}")
    print(f"add(2, 3) = {add(2, 3)}")
    print(f"multiply(4, 5) = {multiply(4, 5)}")

    # --- __name__ distinguishes "run directly" from "imported" ---
    print(f"this file's __name__ = {__name__!r}")
    print(f"mypackage's __name__ = {mypackage.__name__!r}")

    # --- Packages have a __file__ and __path__; plain modules only __file__ ---
    print(f"mypackage.__file__ = {mypackage.__file__}")
    print(f"mypackage.__path__ = {list(mypackage.__path__)}")

    # --- __all__ controls what `import *` pulls in ---
    print(f"mypackage.__all__ = {mypackage.__all__}")

    # --- Re-importing is a no-op: Python caches modules in sys.modules ---
    import sys

    print(f"'mypackage' in sys.modules: {'mypackage' in sys.modules}")

    # --- Underscore-prefixed names are importable but signal "private" ---
    print(f"helpers._internal_only() = {helpers._internal_only()}")


if __name__ == "__main__":
    main()

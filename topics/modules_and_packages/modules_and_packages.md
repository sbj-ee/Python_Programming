# Modules & Packages

A module is any `.py` file. A package is a directory containing
`__init__.py` plus modules (or other packages). Understanding the import
system is understanding how Python finds and caches both.

## Importing

```python
import math                       # module: math.sqrt(4)
import mypackage                  # package: runs mypackage/__init__.py
import mypackage.helpers as h      # explicit submodule import
from mypackage import add          # names re-exported by __init__.py
from mypackage.helpers import add  # reach directly into a submodule

from mypackage import *            # imports everything in __all__ (or
                                     # everything not underscore-prefixed,
                                     # if __all__ isn't defined) -- avoid
                                     # in real code, it pollutes the namespace
```

## __init__.py and __all__

```python
# mypackage/__init__.py
from .helpers import add, multiply
__all__ = ["add", "multiply"]      # controls `from mypackage import *`

# lets callers write: from mypackage import add
# instead of the more verbose: from mypackage.helpers import add
```

## __name__ == "__main__"

```python
# script.py
def main():
    ...

if __name__ == "__main__":   # True only when run directly: python script.py
    main()                    # False when imported: import script
```

This guard is what lets a file serve double duty as both a runnable script
and an importable module without the "script" behavior firing on import.

## sys.path and module caching

```python
import sys
sys.path             # list of directories Python searches for modules
sys.modules           # cache: {"mypackage": <module ...>}

import mypackage      # first import: runs __init__.py, caches the result
import mypackage      # second import: returns the CACHED module, doesn't re-run
```

## Relative vs. absolute imports

```python
# inside mypackage/submodule.py:
from . import helpers            # relative: "this package"
from .helpers import add          # relative: "this package's helpers module"
from ..otherpackage import thing  # relative: "the parent package's otherpackage"

from mypackage import helpers     # absolute: fully-qualified from the top
```

Absolute imports are generally preferred (PEP 8) for clarity; relative
imports are common within a package's own internal structure.

## Namespace packages (PEP 420)

```python
# A directory WITHOUT __init__.py can still be a package in modern Python --
# a "namespace package". Rare in application code; mostly relevant for
# splitting one logical package across multiple installed distributions.
```

## Common pitfalls

| Pitfall | Consequence | Fix |
|---------|-------------|-----|
| Circular imports (`a.py` imports `b.py` which imports `a.py`) | `ImportError` at one of the import statements | Restructure to remove the cycle, or import inside the function that needs it |
| `from module import *` in application code | Namespace pollution, unclear where names come from | Import specific names, or the module itself |
| Naming a file the same as a stdlib module (e.g. `random.py`) | Your file shadows the stdlib module for every import in that directory | Avoid stdlib module names for your own files |
| Running a script inside a package with `python script.py` | Relative imports fail: "attempted relative import with no known parent package" | Run as `python -m package.script`, or restructure to avoid needing relative imports at the entry point |
| Assuming re-importing re-runs top-level code | It doesn't -- `sys.modules` caches the first import | Use `importlib.reload()` only for interactive/dev workflows, never in production logic |

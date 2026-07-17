"""mypackage: demonstrates a real, importable package.

`__init__.py` marks a directory as a regular package and runs whenever the
package (or anything inside it) is first imported. Re-exporting names here
lets callers write `from mypackage import add` instead of reaching into
`mypackage.helpers`.
"""

from .helpers import add, multiply

__all__ = ["add", "multiply"]  # controls `from mypackage import *`

"""src package for the Seufz Counter project.

 Package version so users can do `from src import Counter` and inspect
`src.__version__` without deep modules import.
"""

from src.counter import Counter

__all__ = ["Counter"]
__version__ = "0.1.0"

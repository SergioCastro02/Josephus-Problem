"""Multiple verified approaches to the Josephus problem.

The public API is intentionally small; each solver lives in its own module and
is re-exported here for convenience.
"""

from josephus.simulation import elimination_order, eliminations, survivor

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "elimination_order",
    "eliminations",
    "survivor",
]

"""Multiple verified approaches to the Josephus problem.

Each solver lives in its own module:

- :mod:`josephus.simulation` -- direct ``O(n*k)`` simulation (reference)
- :mod:`josephus.recurrence` -- ``O(n)`` recurrence for the survivor

The names re-exported here point at the fastest available implementation for
each task; import a submodule directly to pick a specific method.
"""

from josephus.recurrence import survivor
from josephus.simulation import elimination_order, eliminations

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "elimination_order",
    "eliminations",
    "survivor",
]

"""Multiple verified approaches to the Josephus problem.

Each solver lives in its own module:

- :mod:`josephus.simulation`  -- direct ``O(n*k)`` simulation (reference)
- :mod:`josephus.recurrence`  -- ``O(n)`` recurrence for the survivor
- :mod:`josephus.closed_form` -- ``O(1)`` closed form, ``k == 2`` only
- :mod:`josephus.fenwick`     -- ``O(n log n)`` full elimination order

:func:`survivor` and :func:`elimination_order` below dispatch to the fastest
available implementation; import a submodule directly to pin a method.
"""

from josephus import closed_form, fenwick, recurrence

__version__ = "0.1.0"

__all__ = [
    "__version__",
    "elimination_order",
    "eliminations",
    "survivor",
]

#: Full elimination order (survivor last) -- Fenwick tree, ``O(n log n)``.
elimination_order = fenwick.elimination_order
eliminations = fenwick.eliminations


def survivor(n: int, k: int) -> int:
    """Return the 0-indexed last survivor for a circle of ``n`` counting ``k``.

    Uses the constant-time closed form when ``k == 2`` and the ``O(n)``
    recurrence otherwise.
    """
    if k == 2:
        return closed_form.survivor(n)
    return recurrence.survivor(n, k)

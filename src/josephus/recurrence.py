"""Closed recurrence for the last survivor.

Let ``J(n, k)`` be the 0-indexed survivor for a circle of ``n`` people counting
every ``k``-th. Removing the first victim (at index ``k - 1``) leaves ``n - 1``
people, and the survivor of that smaller circle -- relabelled so counting
resumes from the person after the victim -- maps back to the original circle by

    J(n, k) = (J(n - 1, k) + k) % n,    with  J(1, k) = 0.

Evaluating it bottom-up is ``O(n)`` time and ``O(1)`` space, and unlike the
simulation it does not depend on ``k`` for its running time.

This recurrence yields only the survivor, not the full elimination order.
"""

from __future__ import annotations


def survivor(n: int, k: int) -> int:
    """Return the position of the last survivor via the Josephus recurrence."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")

    result = 0  # J(1, k)
    for circle_size in range(2, n + 1):
        result = (result + k) % circle_size
    return result

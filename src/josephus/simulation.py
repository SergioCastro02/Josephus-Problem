"""Direct simulation of the elimination process.

This is the slowest approach (``O(n * k)`` time) but the easiest to read, so
it doubles as the reference implementation the other solvers are checked
against.

Positions are 0-indexed: people are numbered ``0 .. n - 1`` and counting starts
at person ``0``.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator


def _validate(n: int, k: int) -> None:
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")


def eliminations(n: int, k: int) -> Iterator[int]:
    """Yield the positions ``0 .. n - 1`` in the order they are eliminated.

    The final value yielded is the last survivor, so the iterator has exactly
    ``n`` elements.
    """
    _validate(n, k)
    circle: deque[int] = deque(range(n))
    while circle:
        # Move the k-th person to the front, then remove them.
        circle.rotate(-(k - 1))
        yield circle.popleft()


def elimination_order(n: int, k: int) -> list[int]:
    """Return every position in elimination order (survivor last)."""
    return list(eliminations(n, k))


def survivor(n: int, k: int) -> int:
    """Return the position of the last survivor."""
    last = -1
    for last in eliminations(n, k):
        pass
    return last

"""Full elimination order in ``O(n log n)`` using a Fenwick tree.

The simulation walks ``k`` steps per elimination, so producing the whole order
costs ``O(n * k)``. Here a Fenwick (binary indexed) tree over ``n`` slots -- 1
for alive, 0 for eliminated -- turns "find the r-th person still alive" into an
``O(log n)`` query, giving ``O(n log n)`` overall regardless of ``k``.

Positions are 0-indexed and counting starts at person 0, matching the rest of
the package.
"""

from __future__ import annotations

from collections import deque
from collections.abc import Iterator


class Fenwick:
    """Fenwick tree supporting point updates and prefix-sum ``find_kth``."""

    __slots__ = ("_n", "_tree")

    def __init__(self, size: int) -> None:
        self._n = size
        self._tree = [0] * (size + 1)

    @classmethod
    def ones(cls, size: int) -> Fenwick:
        """Build a tree of ``size`` slots each holding 1, in ``O(n)``."""
        fw = cls(size)
        tree = fw._tree
        for i in range(1, size + 1):
            tree[i] += 1
            parent = i + (i & -i)
            if parent <= size:
                tree[parent] += tree[i]
        return fw

    def add(self, index: int, delta: int) -> None:
        """Add ``delta`` at 0-indexed ``index``."""
        i = index + 1
        while i <= self._n:
            self._tree[i] += delta
            i += i & -i

    def find_kth(self, k: int) -> int:
        """Return the 0-indexed position with prefix sum ``k`` (``k >= 1``).

        In this module every slot is 0 or 1, so this is "the k-th slot that is
        still set".
        """
        if k < 1:
            raise ValueError(f"k must be >= 1, got {k}")
        pos = 0
        remaining = k
        log = (self._n).bit_length()
        for step in range(log, -1, -1):
            nxt = pos + (1 << step)
            if nxt <= self._n and self._tree[nxt] < remaining:
                pos = nxt
                remaining -= self._tree[nxt]
        if pos >= self._n:
            raise ValueError(f"no slot with prefix sum {k}")
        return pos


def _validate(n: int, k: int) -> None:
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    if k < 1:
        raise ValueError(f"k must be >= 1, got {k}")


def eliminations(n: int, k: int) -> Iterator[int]:
    """Yield positions in elimination order (survivor last), in ``O(n log n)``."""
    _validate(n, k)
    alive_tree = Fenwick.ones(n)
    start = 1  # 1-indexed rank, among the currently alive, where counting begins
    for alive in range(n, 0, -1):
        rank = (start + k - 2) % alive + 1
        victim = alive_tree.find_kth(rank)
        yield victim
        alive_tree.add(victim, -1)
        # The person just after the victim keeps `rank` in the shrunken circle,
        # unless the victim was last, in which case counting wraps to the front.
        start = rank if rank <= alive - 1 else 1


def elimination_order(n: int, k: int) -> list[int]:
    """Return every position in elimination order (survivor last)."""
    return list(eliminations(n, k))


def survivor(n: int, k: int) -> int:
    """Return the position of the last survivor."""
    return deque(eliminations(n, k), maxlen=1)[0]

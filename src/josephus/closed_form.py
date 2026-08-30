"""Constant-time closed form for the special case ``k == 2``.

Write ``n = 2**m + L`` with ``0 <= L < 2**m``. The 1-indexed survivor is then
``2*L + 1``; equivalently, take the binary representation of ``n`` and rotate
its leading 1 bit to the least-significant position. In 0-indexed terms:

    survivor(n) = 2 * (n - 2**floor(log2 n))

Both are ``O(1)`` (ignoring big-integer costs). There is no comparably simple
closed form for general ``k`` -- use :mod:`josephus.recurrence` for that.
"""

from __future__ import annotations


def highest_power_of_two(n: int) -> int:
    """Largest power of two that is ``<= n`` (for ``n >= 1``)."""
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    return 1 << (n.bit_length() - 1)


def survivor(n: int) -> int:
    """Return the 0-indexed last survivor for ``k == 2``."""
    remainder = n - highest_power_of_two(n)
    return 2 * remainder


def survivor_bit_rotation(n: int) -> int:
    """Same result as :func:`survivor`, via the leading-bit-rotation trick.

    Kept as an independent implementation so the two can be checked against
    each other.
    """
    if n < 1:
        raise ValueError(f"n must be >= 1, got {n}")
    bits = n.bit_length()
    leading = 1 << (bits - 1)
    one_indexed = ((n ^ leading) << 1) | 1
    return one_indexed - 1

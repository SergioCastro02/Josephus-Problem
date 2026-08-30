"""Tests for the O(n) recurrence solver."""

from __future__ import annotations

import pytest

from josephus import recurrence


def test_classic_n41_k3():
    assert recurrence.survivor(41, 3) == 30


def test_k1_survivor_is_last_person():
    assert recurrence.survivor(9, 1) == 8


def test_single_person():
    assert recurrence.survivor(1, 5) == 0


def test_k2_matches_known_small_values():
    # 0-indexed survivors for k=2, n = 1..10.
    expected = [0, 0, 2, 0, 2, 4, 6, 0, 2, 4]
    assert [recurrence.survivor(n, 2) for n in range(1, 11)] == expected


@pytest.mark.parametrize(("n", "k"), [(0, 2), (-1, 2), (5, 0), (5, -1)])
def test_invalid_input_raises(n, k):
    with pytest.raises(ValueError):
        recurrence.survivor(n, k)

"""Tests for the reference simulation."""

from __future__ import annotations

import pytest

from josephus.simulation import elimination_order, eliminations, survivor


def test_classic_n41_k3():
    # Historic instance; the survivor is person 31 when numbering from 1.
    assert survivor(41, 3) == 30


def test_small_circle_full_order():
    # n=7, k=3 -> eliminate 3,6,2,7,5,1 then 4 survives (1-indexed).
    assert elimination_order(7, 3) == [2, 5, 1, 6, 4, 0, 3]


def test_k1_eliminates_in_natural_order():
    assert elimination_order(5, 1) == [0, 1, 2, 3, 4]
    assert survivor(5, 1) == 4


def test_single_person_survives_immediately():
    assert elimination_order(1, 7) == [0]
    assert survivor(1, 7) == 0


def test_eliminations_is_a_permutation_of_all_positions():
    n, k = 20, 6
    assert sorted(eliminations(n, k)) == list(range(n))


def test_k_larger_than_n_wraps_around():
    # n=3, k=5: 0,1,2,0,1 -> eliminate 1; then 2,0,2,0,2 -> eliminate 2.
    assert elimination_order(3, 5) == [1, 2, 0]


@pytest.mark.parametrize("n", [0, -1])
def test_invalid_n_raises(n):
    with pytest.raises(ValueError):
        survivor(n, 2)


@pytest.mark.parametrize("k", [0, -3])
def test_invalid_k_raises(k):
    with pytest.raises(ValueError):
        survivor(10, k)

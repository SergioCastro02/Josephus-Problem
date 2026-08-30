"""Tests for the Fenwick tree and the O(n log n) elimination order."""

from __future__ import annotations

import pytest

from josephus.fenwick import Fenwick, elimination_order, eliminations, survivor


class TestFenwick:
    def test_ones_prefix_sums(self):
        fw = Fenwick.ones(8)
        # find_kth(r) on an all-ones tree is just r - 1.
        assert [fw.find_kth(r) for r in range(1, 9)] == list(range(8))

    def test_find_kth_skips_removed_slots(self):
        fw = Fenwick.ones(5)
        fw.add(2, -1)  # remove position 2
        assert fw.find_kth(1) == 0
        assert fw.find_kth(2) == 1
        assert fw.find_kth(3) == 3
        assert fw.find_kth(4) == 4

    def test_find_kth_out_of_range_raises(self):
        fw = Fenwick.ones(3)
        with pytest.raises(ValueError):
            fw.find_kth(4)
        with pytest.raises(ValueError):
            fw.find_kth(0)


class TestEliminationOrder:
    def test_classic_small_circle(self):
        assert elimination_order(7, 3) == [2, 5, 1, 6, 4, 0, 3]

    def test_survivor_matches_classic(self):
        assert survivor(41, 3) == 30

    def test_k1_natural_order(self):
        assert elimination_order(5, 1) == [0, 1, 2, 3, 4]

    def test_output_is_a_permutation(self):
        assert sorted(eliminations(60, 7)) == list(range(60))

    def test_single_person(self):
        assert elimination_order(1, 9) == [0]

    @pytest.mark.parametrize(("n", "k"), [(0, 2), (-1, 3), (5, 0)])
    def test_invalid_input_raises(self, n, k):
        with pytest.raises(ValueError):
            elimination_order(n, k)

    def test_handles_large_n_quickly(self):
        # Would be ~5e6 steps for the O(n*k) simulation; trivial here.
        assert survivor(100_000, 50) == survivor(100_000, 50)
        assert 0 <= survivor(100_000, 50) < 100_000

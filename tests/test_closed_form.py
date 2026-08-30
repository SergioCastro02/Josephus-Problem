"""Tests for the k == 2 closed form."""

from __future__ import annotations

import pytest

from josephus import closed_form


def test_classic_n41():
    # 1-indexed survivor is 19, hence 18 when numbering from 0.
    assert closed_form.survivor(41) == 18


def test_powers_of_two_survivor_is_zero():
    for m in range(12):
        assert closed_form.survivor(1 << m) == 0


def test_one_past_a_power_of_two_survivor_is_two():
    for m in range(1, 12):
        assert closed_form.survivor((1 << m) + 1) == 2


def test_small_values_table():
    expected = [0, 0, 2, 0, 2, 4, 6, 0, 2, 4]  # n = 1..10, 0-indexed
    assert [closed_form.survivor(n) for n in range(1, 11)] == expected


def test_highest_power_of_two():
    assert closed_form.highest_power_of_two(1) == 1
    assert closed_form.highest_power_of_two(2) == 2
    assert closed_form.highest_power_of_two(41) == 32
    assert closed_form.highest_power_of_two(1023) == 512
    assert closed_form.highest_power_of_two(1024) == 1024


def test_two_implementations_agree():
    for n in range(1, 5000):
        assert closed_form.survivor(n) == closed_form.survivor_bit_rotation(n)


@pytest.mark.parametrize("bad", [0, -1, -100])
def test_invalid_n_raises(bad):
    with pytest.raises(ValueError):
        closed_form.survivor(bad)
    with pytest.raises(ValueError):
        closed_form.survivor_bit_rotation(bad)

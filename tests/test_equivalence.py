"""Cross-checks between the different solvers.

Every approach must agree with the reference simulation. As more solvers are
added they get plugged in here.
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

import josephus
from josephus import closed_form, fenwick, recurrence, simulation

_n = st.integers(min_value=1, max_value=300)
_k = st.integers(min_value=1, max_value=50)


@given(n=_n, k=_k)
def test_recurrence_matches_simulation(n, k):
    assert recurrence.survivor(n, k) == simulation.survivor(n, k)


@given(n=_n)
def test_closed_form_matches_simulation_for_k2(n):
    assert closed_form.survivor(n) == simulation.survivor(n, 2)


@given(n=_n, k=_k)
def test_package_survivor_matches_simulation(n, k):
    assert josephus.survivor(n, k) == simulation.survivor(n, k)


@given(n=_n, k=_k)
def test_fenwick_order_matches_simulation(n, k):
    assert fenwick.elimination_order(n, k) == simulation.elimination_order(n, k)

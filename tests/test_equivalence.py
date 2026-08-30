"""Cross-checks between the different solvers.

Every approach must agree with the reference simulation. As more solvers are
added they get plugged in here.
"""

from __future__ import annotations

from hypothesis import given
from hypothesis import strategies as st

from josephus import recurrence, simulation

_n = st.integers(min_value=1, max_value=300)
_k = st.integers(min_value=1, max_value=50)


@given(n=_n, k=_k)
def test_recurrence_matches_simulation(n, k):
    assert recurrence.survivor(n, k) == simulation.survivor(n, k)

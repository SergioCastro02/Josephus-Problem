"""Tests for the command-line interface."""

from __future__ import annotations

import json

import pytest

from josephus.cli import main


def test_survivor_default(capsys):
    assert main(["41", "3"]) == 0
    assert capsys.readouterr().out.strip() == "30"


def test_k_defaults_to_two(capsys):
    assert main(["41"]) == 0
    assert capsys.readouterr().out.strip() == "18"


def test_one_indexed(capsys):
    main(["41", "3", "--one-indexed"])
    assert capsys.readouterr().out.strip() == "31"


def test_order(capsys):
    main(["7", "3", "--order"])
    assert capsys.readouterr().out.strip() == "2 5 1 6 4 0 3"


def test_order_one_indexed(capsys):
    main(["7", "3", "--order", "--one-indexed"])
    assert capsys.readouterr().out.strip() == "3 6 2 7 5 1 4"


def test_json_survivor(capsys):
    main(["41", "3", "--json"])
    assert json.loads(capsys.readouterr().out) == {"n": 41, "k": 3, "survivor": 30}


def test_json_order(capsys):
    main(["5", "2", "--order", "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert payload == {"n": 5, "k": 2, "elimination_order": [1, 3, 0, 4, 2]}


@pytest.mark.parametrize("method", ["auto", "simulation", "recurrence", "fenwick"])
def test_methods_agree_on_survivor(method, capsys):
    from josephus import simulation

    expected = str(simulation.survivor(23, 5))
    main(["23", "5", "--method", method])
    assert capsys.readouterr().out.strip() == expected


def test_closed_form_method_rejects_non_two_k(capsys):
    with pytest.raises(SystemExit):
        main(["10", "3", "--method", "closed-form"])


def test_order_with_recurrence_method_is_rejected():
    with pytest.raises(SystemExit):
        main(["10", "3", "--order", "--method", "recurrence"])


def test_invalid_n_exits_2(capsys):
    assert main(["0", "3"]) == 2
    assert "error:" in capsys.readouterr().err

"""Command-line interface: ``josephus`` / ``python -m josephus``.

Examples
--------
    josephus 41 3                 -> 30            (0-indexed survivor)
    josephus 41 3 --one-indexed   -> 31
    josephus 7 3 --order          -> 2 5 1 6 4 0 3
    josephus 1000000 2 --method closed-form
    josephus 7 3 --order --json
"""

from __future__ import annotations

import argparse
import json
import sys
from collections.abc import Sequence

from josephus import __version__, closed_form, fenwick, recurrence, simulation

_SURVIVOR_METHODS = {
    "auto": None,
    "simulation": simulation.survivor,
    "recurrence": recurrence.survivor,
    "fenwick": fenwick.survivor,
    "closed-form": lambda n, k: closed_form.survivor(n),
}
_ORDER_METHODS = {
    "auto": fenwick.elimination_order,
    "simulation": simulation.elimination_order,
    "fenwick": fenwick.elimination_order,
}


def _auto_survivor(n: int, k: int) -> int:
    return closed_form.survivor(n) if k == 2 else recurrence.survivor(n, k)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="josephus",
        description="Solve the Josephus problem (0-indexed, counting starts at 0).",
    )
    parser.add_argument("n", type=int, help="number of people in the circle (>= 1)")
    parser.add_argument(
        "k", type=int, nargs="?", default=2, help="count for elimination (default: 2)"
    )
    parser.add_argument(
        "--order",
        action="store_true",
        help="print the full elimination order instead of just the survivor",
    )
    parser.add_argument(
        "--method",
        default="auto",
        choices=sorted(set(_SURVIVOR_METHODS) | set(_ORDER_METHODS)),
        help="force a specific algorithm (default: auto)",
    )
    parser.add_argument(
        "--one-indexed",
        action="store_true",
        help="number people from 1 instead of 0",
    )
    parser.add_argument("--json", action="store_true", help="emit JSON")
    parser.add_argument(
        "--version", action="version", version=f"%(prog)s {__version__}"
    )
    return parser


def _resolve(args: argparse.Namespace):
    if args.order:
        if args.method not in _ORDER_METHODS:
            raise SystemExit(
                f"--method {args.method} has no elimination-order implementation "
                f"(try: {', '.join(sorted(_ORDER_METHODS))})"
            )
        return _ORDER_METHODS[args.method](args.n, args.k)
    if args.method == "auto":
        return _auto_survivor(args.n, args.k)
    if args.method == "closed-form" and args.k != 2:
        raise SystemExit("--method closed-form only applies to k == 2")
    return _SURVIVOR_METHODS[args.method](args.n, args.k)


def main(argv: Sequence[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        result = _resolve(args)
    except ValueError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2

    shift = 1 if args.one_indexed else 0
    if isinstance(result, list):
        values = [p + shift for p in result]
        if args.json:
            print(json.dumps({"n": args.n, "k": args.k, "elimination_order": values}))
        else:
            print(" ".join(map(str, values)))
    else:
        value = result + shift
        if args.json:
            print(json.dumps({"n": args.n, "k": args.k, "survivor": value}))
        else:
            print(value)
    return 0


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())

"""Time the four survivor solvers across a range of circle sizes.

    python benchmarks/bench.py                  # quick run, markdown table
    python benchmarks/bench.py --max-n 2000000  # push it further
    python benchmarks/bench.py --csv results/bench.csv --plot

``--plot`` needs the ``bench`` extra:  pip install -e ".[bench]"
"""

from __future__ import annotations

import argparse
import csv
import sys
import time
from collections.abc import Callable, Sequence
from pathlib import Path

from josephus import closed_form, fenwick, recurrence, simulation

Solver = Callable[[int, int], int]

SOLVERS: dict[str, tuple[Solver, str]] = {
    "simulation": (simulation.survivor, "O(n*k)"),
    "recurrence": (recurrence.survivor, "O(n)"),
    "fenwick": (fenwick.survivor, "O(n log n)"),
    "closed_form": (lambda n, k: closed_form.survivor(n), "O(1)"),
}

DEFAULT_SIZES = [1_000, 10_000, 50_000, 100_000, 250_000]
ORDER_SIZES = [5_000, 25_000, 50_000, 100_000, 200_000]


def _time(fn: Solver, n: int, k: int, repeats: int) -> float:
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        fn(n, k)
        best = min(best, time.perf_counter() - start)
    return best


def run(sizes: Sequence[int], k: int, repeats: int) -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for n in sizes:
        row: dict[str, object] = {"n": n}
        reference = None
        for name, (fn, _) in SOLVERS.items():
            if name == "simulation" and n > 200_000:
                row[name] = None  # too slow to be worth waiting for
                continue
            value = fn(n, k)
            if name == "closed_form" and k != 2:
                row[name] = None
                continue
            if reference is None:
                reference = value
            elif value != reference:
                raise AssertionError(
                    f"{name}({n}, {k}) = {value}, expected {reference}"
                )
            row[name] = _time(fn, n, k, repeats)
        rows.append(row)
    return rows


def run_order(sizes: Sequence[int], repeats: int) -> list[dict[str, object]]:
    """Full elimination order with k = n // 2 -- the regime where O(n*k)
    simulation degrades to O(n^2) and the Fenwick tree pulls ahead."""
    rows: list[dict[str, object]] = []
    backends = {
        "simulation": simulation.elimination_order,
        "fenwick": fenwick.elimination_order,
    }
    for n in sizes:
        k = max(2, n // 2)
        row: dict[str, object] = {"n": n, "k": k}
        reference = None
        for name, fn in backends.items():
            if name == "simulation" and n > 100_000:
                row[name] = None
                continue
            result = fn(n, k)
            if reference is None:
                reference = result
            elif result != reference:
                raise AssertionError(f"{name} disagrees at n={n}, k={k}")
            best = float("inf")
            for _ in range(repeats):
                start = time.perf_counter()
                fn(n, k)
                best = min(best, time.perf_counter() - start)
            row[name] = best
        rows.append(row)
    return rows


def order_markdown(rows: list[dict[str, object]]) -> str:
    lines = [
        "Full elimination order, k = n // 2, timings in milliseconds.",
        "",
        "| n | k | simulation | fenwick |",
        "|---|---|---|---|",
    ]
    for row in rows:
        sim = row.get("simulation")
        fen = row.get("fenwick")
        lines.append(
            f"| {row['n']:,} | {row['k']:,} | "
            f"{'-' if sim is None else f'{sim * 1000:.1f}'} | "
            f"{'-' if fen is None else f'{fen * 1000:.1f}'} |"
        )
    return "\n".join(lines)


def to_markdown(rows: list[dict[str, object]], k: int) -> str:
    names = list(SOLVERS)
    header = f"| n | {' | '.join(names)} |"
    sep = "|" + "---|" * (len(names) + 1)
    lines = [f"Timings in milliseconds, k = {k} (best of N repeats).", "", header, sep]
    for row in rows:
        cells = []
        for name in names:
            val = row.get(name)
            cells.append("-" if val is None else f"{val * 1000:.2f}")
        lines.append(f"| {row['n']:,} | {' | '.join(cells)} |")
    return "\n".join(lines)


def write_csv(rows: list[dict[str, object]], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="") as fh:
        writer = csv.DictWriter(fh, fieldnames=["n", *SOLVERS])
        writer.writeheader()
        writer.writerows(rows)


def make_plot(rows: list[dict[str, object]], path: Path) -> None:
    try:
        import matplotlib.pyplot as plt
    except ImportError:
        sys.exit('--plot needs matplotlib: pip install -e ".[bench]"')

    path.parent.mkdir(parents=True, exist_ok=True)
    ns = [row["n"] for row in rows]
    fig, ax = plt.subplots()
    for name in SOLVERS:
        ys = [
            (row[name] * 1000 if row.get(name) is not None else None) for row in rows
        ]
        pairs = [(n, y) for n, y in zip(ns, ys) if y is not None]
        if pairs:
            ax.plot(*zip(*pairs), marker="o", label=name)
    ax.set_xlabel("n")
    ax.set_ylabel("time (ms)")
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.legend()
    ax.set_title("Josephus survivor: solver timings")
    fig.tight_layout()
    fig.savefig(path, dpi=120)


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--k", type=int, default=2)
    parser.add_argument("--max-n", type=int, default=None, help="cap on circle size")
    parser.add_argument("--repeats", type=int, default=5)
    parser.add_argument("--csv", type=Path, default=None)
    parser.add_argument("--plot", nargs="?", const=Path("benchmarks/results/bench.png"))
    args = parser.parse_args(argv)

    sizes = DEFAULT_SIZES
    if args.max_n is not None:
        sizes = [n for n in DEFAULT_SIZES if n <= args.max_n] or [args.max_n]
        if args.max_n not in sizes:
            sizes = [*sizes, args.max_n]

    rows = run(sizes, args.k, args.repeats)
    print(to_markdown(rows, args.k))
    print()
    order_sizes = ORDER_SIZES
    if args.max_n is not None:
        order_sizes = [n for n in ORDER_SIZES if n <= args.max_n] or [args.max_n]
    print(order_markdown(run_order(order_sizes, args.repeats)))
    if args.csv:
        write_csv(rows, args.csv)
        print(f"\nwrote {args.csv}")
    if args.plot:
        make_plot(rows, Path(args.plot))
        print(f"wrote {args.plot}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

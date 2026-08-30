# Josephus Problem

Multiple approaches to the Josephus problem in Python, from a straightforward
simulation to a closed-form solution, each verified against the others.

## The problem

`n` people stand in a circle, numbered `0` to `n - 1`. Starting the count at
person `0`, every `k`-th person is eliminated, and counting continues from the
next person. The task is to find the position of the last survivor (and,
optionally, the full order in which people are eliminated).

## Benchmarks

Reproduce with `python benchmarks/bench.py` (CPython 3.14, best of 5 runs;
absolute numbers are machine-dependent, the shape is not).

Survivor only, `k = 2`, time in ms:

| n | simulation | recurrence | fenwick | closed_form |
|---|---|---|---|---|
| 1,000 | 0.09 | 0.03 | 1.79 | 0.00 |
| 10,000 | 0.97 | 0.36 | 23.19 | 0.00 |
| 50,000 | 4.91 | 1.89 | 129.82 | 0.00 |
| 100,000 | 10.17 | 3.77 | 274.58 | 0.00 |
| 250,000 | — | 9.25 | 721.62 | 0.00 |

For the survivor alone the recurrence wins outright (and the closed form is
free). The Fenwick tree is the slowest here — its `find_kth` pays an
`O(log n)` cost per elimination for a query the other methods do not need.

Full elimination order, `k = n // 2`, time in ms:

| n | simulation | fenwick |
|---|---|---|
| 5,000 | 1.8 | 10.7 |
| 25,000 | 32.8 | 61.1 |
| 50,000 | 137.3 | 131.5 |
| 100,000 | 589.0 | 285.8 |
| 200,000 | — | 611.2 |

The deque simulation's `rotate` is a C-level operation, so it stays
competitive far longer than its `O(n·k)` label suggests, but once `k` grows
with `n` the Fenwick tree's `O(n log n)` pulls clearly ahead (crossover near
`n = 50,000` here).

## Development

```bash
python -m pip install -e ".[dev]"
pytest
ruff check .
```

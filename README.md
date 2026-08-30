# Josephus Problem

[![CI](https://github.com/SergioCastro02/Josephus-Problem/actions/workflows/ci.yml/badge.svg)](https://github.com/SergioCastro02/Josephus-Problem/actions/workflows/ci.yml)

Four approaches to the Josephus problem in Python — simulation, an `O(n)`
recurrence, an `O(1)` closed form for `k = 2`, and an `O(n log n)` Fenwick
tree for the full elimination order — each cross-checked against the others
with property-based tests.

## The problem

`n` people stand in a circle, numbered `0` to `n - 1`. Counting starts at
person `0`; every `k`-th person is eliminated and counting resumes from the
next surviving person. Two questions:

1. **Who survives?** — the position of the last person left.
2. **In what order does everyone go?** — the full elimination sequence.

Named after Flavius Josephus, who (by his account) survived a 41-man suicide
pact by working out where to stand. For `n = 41, k = 3` the survivor is
position `30` (person `31` counting from 1).

All functions in this package are **0-indexed** and count starting at person
`0`. Pass `--one-indexed` on the CLI for 1-indexed output.

## Install

```bash
git clone https://github.com/SergioCastro02/Josephus-Problem.git
cd Josephus-Problem
python -m pip install -e ".[dev]"
```

## Usage

### Library

```python
import josephus

josephus.survivor(41, 3)            # -> 30
josephus.survivor(1_000_000, 2)     # -> 951424  (closed form, instant)
josephus.elimination_order(7, 3)    # -> [2, 5, 1, 6, 4, 0, 3]

# Pick a specific method:
from josephus import simulation, recurrence, closed_form, fenwick
recurrence.survivor(41, 3)          # -> 30
closed_form.survivor(41)            # -> 18   (k = 2 only)
fenwick.elimination_order(10**6, 500_000)   # O(n log n)
```

### Command line

```bash
josephus 41 3                 # 30
josephus 41 3 --one-indexed   # 31
josephus 41                   # 18   (k defaults to 2)
josephus 7 3 --order          # 2 5 1 6 4 0 3
josephus 7 3 --order --json   # {"n": 7, "k": 3, "elimination_order": [...]}
josephus 1000000 2 --method closed-form
```

`python -m josephus ...` works too.

## The four approaches

| module | solves | time | space | notes |
|---|---|---|---|---|
| `simulation` | survivor + order | `O(n·k)`* | `O(n)` | reference implementation; a `deque` whose C-level `rotate` keeps it fast in practice |
| `recurrence` | survivor | `O(n)` | `O(1)` | best choice for the survivor at any `k` |
| `closed_form` | survivor | `O(1)` | `O(1)` | `k = 2` only |
| `fenwick` | survivor + order | `O(n log n)` | `O(n)` | best choice for the full order when `k` is large |

\* `deque.rotate` runs in C, so the practical crossover with the Fenwick tree
is much later than the asymptotics suggest — see [Benchmarks](#benchmarks).

### Recurrence

Let `J(n, k)` be the 0-indexed survivor. The first victim sits at index
`k - 1`; removing them leaves `n - 1` people, and re-indexing from the next
person gives

```
J(n, k) = (J(n - 1, k) + k) % n,      J(1, k) = 0
```

Evaluated bottom-up: `O(n)` time, `O(1)` space, no recursion depth limit,
independent of `k`.

### Closed form (`k = 2`)

Write `n = 2^m + L` with `0 ≤ L < 2^m`. Then the survivor is

```
J(n, 2) = 2L        (0-indexed)
        = 2L + 1    (1-indexed)
```

i.e. take the binary representation of `n` and rotate its leading `1` to the
end. `closed_form` ships this and an independent bit-rotation implementation
that the tests check against each other up to `n = 5000`.

### Fenwick tree (full order)

Keep a binary indexed tree over `n` slots (`1` = alive). "Find the `r`-th
person still alive" becomes an `O(log n)` prefix-sum search, so producing the
whole elimination order costs `O(n log n)` regardless of `k`, versus `O(n·k)`
for stepping through the circle. `fenwick.Fenwick` is a reusable tree with an
`O(n)` `ones()` builder and `find_kth`.

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

Once `k` grows with `n` the Fenwick tree's `O(n log n)` pulls clearly ahead
(crossover near `n = 50,000` here).

## Tests

```bash
pytest            # unit tests + hypothesis equivalence checks
ruff check .      # lint
```

`tests/test_equivalence.py` uses [Hypothesis](https://hypothesis.works/) to
assert that every solver agrees with the reference simulation over randomised
`(n, k)`.

## Project layout

```
src/josephus/
  simulation.py    deque simulation (reference)
  recurrence.py    O(n) recurrence
  closed_form.py   O(1) closed form, k = 2
  fenwick.py       Fenwick tree + O(n log n) order
  cli.py           argparse CLI
tests/             pytest + hypothesis
benchmarks/bench.py
```

## License

MIT — see [LICENSE](LICENSE).

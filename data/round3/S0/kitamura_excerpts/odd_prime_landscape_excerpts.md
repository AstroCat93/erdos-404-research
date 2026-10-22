# Excerpts from K. Kitamura, github.com/KitaKen1/erdos-404-odd-prime-landscape
# Commit ef0881bb4f94da2e52de407dfaaea5acdb3adfcd (2026-07-08 10:54:03 +0900), branch main; cloned 2026-10-13 ~05:55 UTC.
# Licensed Apache-2.0 by the repository owner; reproduced verbatim (excerpts) for citation.

## README.md, lines 1-40

# Erdos #404 at odd primes

[Erdos Problem #404](https://www.erdosproblems.com/404) asks about the
function `f(a,p)`, where `f(a,p) >= K` means that there is a finite
increasing list

```text
a = a_1 < a_2 < ... < a_n
```

such that

```text
p^K | a_1! + a_2! + ... + a_n!.
```

This is an attempt repository for the odd-prime columns
`p = 3, 5, 7, 11, 13`.

- Contribution 1: explicit large finite witnesses for `f(1,p)`.
- Contribution 2: a small `(a,p)` landscape with exact rows and
  baseline lower bounds for `a > 1`.

You can visually inspect the witness table and ignition landscape on
GitHub Pages here:
[https://kitaken1.github.io/erdos-404-odd-prime-landscape/](https://kitaken1.github.io/erdos-404-odd-prime-landscape/).

## Contribution 1: large finite witnesses for `f(1,p)`

The first contribution is a set of explicit finite lower-bound
certificates starting at `a = 1`.

| p | claim | terms | largest index | witness file |
|---:|---:|---:|---:|---|
| 3 | `f(1,3) >= 20000` | 17,355 | 40,010 | `data/f13_ge20000_witness.txt` |
| 5 | `f(1,5) >= 20000` | 24,347 | 80,002 | `data/f15_ge20000_witness.txt` |
| 7 | `f(1,7) >= 20000` | 26,903 | 120,002 | `data/f17_ge20000_witness.txt` |
| 11 | `f(1,11) >= 5000` | 9,009 | 50,007 | `data/f111_ge5000_witness.txt` |
| 13 | `f(1,13) >= 5000` | 9,007 | 59,999 | `data/f113_ge5000_witness.txt` |


## README.md, lines 145-250 (Contribution 2)

## Contribution 2: exact rows and lower bounds for `a > 1`

The second contribution is the `(a,p)` table for starts beyond `a = 1`.
The visual page gives the full compact table.  A small excerpt is:

| a | p=3 | p=5 | p=7 | p=11 | p=13 |
|---:|---:|---:|---:|---:|---:|
| 1 | `>=20000` | `>=20000` | `>=20000` | `>=5000` | `>=5000` |
| 2 | `=0` | `=0` | `>=0 scan` | `>=0 scan` | `>=0 scan` |
| 3 | `=3` | `>=0 scan` | `>=0 scan` | `>=0 scan` | `>=0 scan` |
| 4 | `>=1 scan` | `=0` | `=0` | `>=0 scan` | `>=0 scan` |
| 5 | `=1` | `>=1 scan` | `>=0 scan` | `>=0 scan` | `>=0 scan` |
| 6 | `=3` | `>=1 scan` | `=0` | `>=0 scan` | `>=0 scan` |
| 7 | `>=2 scan` | `=1` | `>=1 scan` | `=0` | `>=0 scan` |
| 8 | `=2` | `>=1 scan` | `>=1 scan` | `=0` | `>=0 scan` |
| 9 | `>=4 scan` | `=1` | `>=1 scan` | `>=0 scan` | `=0` |
| 10 | `>=4 scan` | `>=2 scan` | `>=1 scan` | `=0` | `=0` |
| 11 | `=4` | `>=2 scan` | `=1` | `>=1 scan` | `>=0 scan` |
| 12 | `>=5 scan` | `=2` | `>=1 scan` | `>=1 scan` | `=0` |

This table records two kinds of information.

Here `v_p(N)` denotes the exponent of `p` in `N`; equivalently,
`p^v_p(N)` is the highest power of `p` dividing `N`.

1. Exact rows: a finite DP proves `f(a,p) >= K` and also rules out
   `f(a,p) >= K+1`, so the table records `f(a,p) = K`.
2. Open scan-survivor rows: the start has not died in the scanned
   ignition layer.  These rows still have the baseline one-term witness
   `(a_1) = (a)`, hence

```text
f(a,p) >= v_p(a!).
```

What remains open is the extra exponent beyond `v_p(a!)`.

### Exact rows from the scan

| statement | normalized extra `g = f(a,p) - v_p(a!)` |
|---|---:|
| `f(3,3) = 3` | 2 |
| `f(39,3) = 25` | 7 |
| `f(700,3) = 363` | 18 |
| `f(110,5) = 30` | 4 |
| `f(236,5) = 61` | 4 |
| `f(42,7) = 7` | 1 |
| `f(113,11) = 11` | 1 |
| `f(163,13) = 13` | 1 |

Small exact examples also have separate Lean4Web files:

| statement | Lean4Web file |
|---|---|
| `f(3,3) = 3` | `lean/S404_3_3_exact_lean4web.lean` |
| `f(4,7) = 0` | `lean/S404_4_7_exact_lean4web.lean` |
| `f(6,7) = 0` | `lean/S404_6_7_exact_lean4web.lean` |

### Ignition layer

For exact or no-witness checks at a fixed exponent, the problem becomes
finite.  By Legendre's formula,

```text
v_p(n!) = floor(n/p) + floor(n/p^2) + floor(n/p^3) + ...
```

so once `v_p(n!) >= K`, all later factorials vanish modulo `p^K`.
That gives a finite residue search.

The scan uses the normalized quantity

```text
g(a,p) = f(a,p) - v_p(a!).
```

These are lower bounds coming from the scan-survivor side of the table.
They use the baseline one-term witness `(a_1) = (a)`.

| statement | witness |
|---|---|
| `f(4,3) >= 1` | `(a_1) = (4)` |
| `f(40,3) >= 18` | `(a_1) = (40)` |
| `f(300,5) >= 74` | `(a_1) = (300)` |
| `f(294,7) >= 48` | `(a_1) = (294)` |
| `f(297,11) >= 29` | `(a_1) = (297)` |
| `f(299,13) >= 24` | `(a_1) = (299)` |

In `index.html`, these scan-survivor rows are shown as lower bounds
with a `scan` label.  They are lower bounds, not exact values.

Summary of the current scan:

| p | scanned a | blocked / g=0 exact | positive finite exact | ignited candidates | max finite g |
|---:|---:|---:|---:|---:|---:|
| 3 | `1..2000` | 667 | 600 | 733 | 18 |
| 5 | `1..300` | 120 | 19 | 161 | 4 |
| 7 | `1..300` | 86 | 24 | 190 | 1 |
| 11 | `1..300` | 81 | 6 | 213 | 1 |
| 13 | `1..300` | 69 | 2 | 229 | 1 |

Here "ignited candidate" means only that no finite death was found in
the scanned ignition layer.  It is not a proof that `f(a,p)` is
infinite.

## Files

## README.md, lines 317-382 (Appendix)

## Appendix: observations worth noticing

These are not all final theorems; they are the main patterns suggested
by the current data.

### Baseline lower bound for every `a`

For every `a` and `p`, the one-term list `(a_1) = (a)` gives

```text
f(a,p) >= v_p(a!).
```

This is why open scan-survivor rows should not be displayed as empty.
They always have at least this lower-bound certificate.

### The trivial exact family

If

```text
a == -1 mod p,
```

then every later normalized product is divisible by `p`, so the
normalized sum stays `1 mod p`.  Therefore no extra p-adic digit can be
gained:

```text
f(a,p) = v_p(a!).
```

This accounts for the `trivial_blocked_exact` rows.

### The odd-prime scan looks very uneven

The current finite exact layer is much richer for `p = 3` than for the
larger odd primes in this scan.  The largest observed finite extra
exponent is

```text
g(700,3) = 18,    f(700,3) = 363.
```

For comparison, the largest finite extra exponent currently found is
`4` for `p = 5`, and only `1` for `p = 7, 11, 13`.

### Residue patterns to audit further

Two residue-family patterns currently stand out:

```text
a ==  6 mod 9    gives g(a,3) = 1    in the scanned rows
a == -5 mod 125  gives g(a,5) = 2    in the scanned rows
```

These are observations from the current data and should be audited
before being stated as theorems.

### Open rows are the real question

For many starts, especially as `p` grows, the scan does not produce a
finite death.  These rows have the baseline lower bound
`f(a,p) >= v_p(a!)`, but the extra exponent is unresolved.  The central
question is whether such rows eventually die at some larger finite
exponent, or whether some of them support unbounded behavior.

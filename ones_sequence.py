"""Integers with exactly p ones in binary, listed in increasing order.

The sequence lists every way to choose p bit positions, so its terms, gaps
and group sizes all come from binomial coefficients and powers of 2.

Notation
    p  number of 1s in each integer
    n  0-based position in the sequence
    i  top-bit position; group i holds the integers 2^i .. 2^(i+1)-1,
       labelled "group 2^(i+1)-1" in the workbook (7, 15, 31, ...)

Run ``python ones_sequence.py --help`` for the command line.
"""
from __future__ import annotations

import argparse
from itertools import combinations, islice
from math import comb
from typing import Iterator


# ---------------------------------------------------------------- terms

def nth_term(n: int, p: int) -> int:
    """n-th integer (0-based) with exactly p ones.

    Combinatorial number system: write n = C(c_p,p) + ... + C(c_1,1) with
    c_p > ... > c_1 >= 0, choosing the largest c at each step.
    The term is 2^c_p + ... + 2^c_1.
    """
    if p < 1 or n < 0:
        raise ValueError("need p >= 1 and n >= 0")
    x = 0
    for t in range(p, 0, -1):
        c = t - 1
        while comb(c + 1, t) <= n:
            c += 1
        n -= comb(c, t)
        x |= 1 << c
    return x


def index_of(x: int) -> int:
    """0-based position of x in the sequence for its own number of 1s."""
    if x < 1:
        raise ValueError("x must be positive")
    return sum(comb(c, t) for t, c in enumerate(bit_positions(x), 1))


def bit_positions(x: int) -> list[int]:
    """Positions of the 1 bits of x, lowest first."""
    return [b for b in range(x.bit_length()) if x >> b & 1]


def next_same_ones(x: int) -> int:
    """Next integer after x with the same number of 1s (Gosper's hack)."""
    c = x & -x               # lowest 1 bit
    r = x + c
    return r | ((r ^ x) // c >> 2)


def sequence(p: int, start: int = 0) -> Iterator[int]:
    """Endless sequence of integers with p ones, from position ``start``."""
    x = nth_term(start, p)
    while True:
        yield x
        x = next_same_ones(x)


# ---------------------------------------------------------- differences

def difference(x: int) -> int:
    """x minus the previous term with the same number of 1s.

    r = number of trailing 1s of x, m = position of the next 1 above them:
        difference = 2^(m-r-1) + (2^r - 1)
    The first term 2^p - 1 is measured from 0.
    """
    c = bit_positions(x)
    p = len(c)
    if x == (1 << p) - 1:
        return x
    r = 0
    while c[r] == r:
        r += 1
    return 2 ** (c[r] - r - 1) + 2 ** r - 1


def differences(p: int, count: int) -> list[int]:
    """First ``count`` differences of the p-ones sequence."""
    return [difference(x) for x in islice(sequence(p), count)]


# --------------------------------------------------------------- groups

def group_size(i: int, p: int) -> int:
    """How many integers with p ones have their top bit at i: C(i, p-1)."""
    return comb(i, p - 1)


def group_terms(i: int, p: int) -> list[int]:
    """Integers with p ones and top bit i, ascending."""
    top = 1 << i
    return sorted(top | sum(1 << b for b in bits) for bits in combinations(range(i), p - 1))


def group_differences(i: int, p: int) -> list[int]:
    """Differences for group i, read off the terms."""
    return [difference(x) for x in group_terms(i, p)]


def build_group_differences(i: int, p: int) -> list[int]:
    """Group i's differences built group to group, as in the workbook.

        G_p(p-1)  = [2^p - 1]                         (the start)
        G_p(i+1)  = [a + 2^(i-p)] + G_p(i)[1:] + G_{p-1}(i)

    Add the doubling increment to the first difference, copy the rest, and
    append the matching group from the sequence with one fewer 1.
    For p = 1 every group is the single difference 2^(i-1) (1 for i = 0).
    """
    if i < p - 1:
        return []
    if p == 1:
        return [1 if i == 0 else 2 ** (i - 1)]
    if i == p - 1:
        return [2 ** p - 1]
    prev = build_group_differences(i - 1, p)
    if i == p:                       # seed: first diff is 2^(p-1), not a+inc
        first = 2 ** (p - 1)
    else:
        first = prev[0] + 2 ** (i - 1 - p)
    return [first] + prev[1:] + build_group_differences(i - 1, p - 1)


def build_group_differences_blocks(i: int, p: int) -> list[int]:
    """Group i's differences from the previous group alone (Book1.xlsx, 2012).

        G_p(p)    = [2^(p-1), ..., 2, 1]              (every position starts a block)
        G_p(i+1)  = for each block start s of G_p(i): [G_p(i)[s] + 2^(i-p)] + G_p(i)[s+1:]

    Each block is a tail of the previous group with the increment added to its
    first difference. There are p blocks, and where they start in the new group
    are the next group's block starts. Same result as build_group_differences,
    without using the sequence with one fewer 1.
    """
    if i < p - 1:
        return []
    if i == p - 1:
        return [2 ** p - 1]
    return _blocks(i, p)[0]


def _blocks(i: int, p: int) -> tuple[list[int], list[int]]:
    """(differences, block starts) of group i >= p under the block rule."""
    if i == p:
        return [2 ** k for k in range(p - 1, -1, -1)], list(range(p))
    prev, starts = _blocks(i - 1, p)
    inc = 2 ** (i - 1 - p)
    d, new_starts = [], []
    for s in starts:
        new_starts.append(len(d))
        d += [prev[s] + inc] + prev[s + 1:]
    return d, new_starts


def group_sum(i: int, p: int) -> int:
    """Sum of a group's differences: (2^p-1)*2^(i-p), doubling each group."""
    return 2 ** p - 1 if i == p - 1 else (2 ** p - 1) * 2 ** (i - p)


# ------------------------------------------------------------------ cli

def main() -> None:
    ap = argparse.ArgumentParser(description="Integers with exactly p ones in binary.")
    ap.add_argument("-p", "--ones", type=int, default=3, help="number of 1s (default 3)")
    ap.add_argument("-b", "--bits", type=int, default=8, help="list groups up to this many bits (default 8)")
    ap.add_argument("--nth", type=int, help="print only the n-th term (0-based)")
    args = ap.parse_args()
    p = args.ones

    if args.nth is not None:
        x = nth_term(args.nth, p)
        print(f"term {args.nth} with {p} ones: {x}  ({x:b})  difference {difference(x)}")
        return

    width = args.bits
    print(f"{'group':>7} {'seq':>4} {'binary':>{width}} {'integer':>8} {'diff':>6}")
    for i in range(p - 1, args.bits):
        for k, (x, d) in enumerate(zip(group_terms(i, p), build_group_differences(i, p)), 1):
            label = str(2 ** (i + 1) - 1) if k == 1 else ""
            print(f"{label:>7} {k:>4} {x:>0{width}b} {x:>8} {d:>6}")
        print(f"{'':>7} size C({i},{p - 1}) = {group_size(i, p)}, sum of diffs = {group_sum(i, p)}")


if __name__ == "__main__":
    main()

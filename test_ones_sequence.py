"""Check every formula in ones_sequence against brute force.  Run: pytest"""
from itertools import islice
from math import comb

import pytest

from ones_sequence import (
    build_group_differences, build_group_differences_blocks, difference, group_differences, group_size, group_sum,
    index_of, next_same_ones, nth_term, sequence,
)

BITS = 16
PS = range(1, 7)


def brute(p):
    return [x for x in range(1, 1 << BITS) if bin(x).count("1") == p]


@pytest.mark.parametrize("p", PS)
def test_nth_term_and_index(p):
    for n, x in enumerate(brute(p)):
        assert nth_term(n, p) == x
        assert index_of(x) == n


@pytest.mark.parametrize("p", PS)
def test_gosper_sequence(p):
    s = brute(p)
    assert list(islice(sequence(p), len(s))) == s
    assert all(next_same_ones(a) == b for a, b in zip(s, s[1:]))


@pytest.mark.parametrize("p", PS)
def test_difference(p):
    s = brute(p)
    assert [difference(x) for x in s] == [b - a for a, b in zip([0] + s, s)]


@pytest.mark.parametrize("p", PS)
def test_group_rule_and_facts(p):
    for i in range(p - 1, BITS):
        d = group_differences(i, p)
        assert build_group_differences(i, p) == d
        assert build_group_differences_blocks(i, p) == d
        assert len(d) == group_size(i, p) == comb(i, p - 1)
        assert sum(d) == group_sum(i, p)
        if i >= p:
            assert d[-1] == 2 ** (i - p)
        if p >= 2:
            assert d.count(1) == (comb(i - 2, p - 2) if i >= 2 else 0)


@pytest.mark.parametrize("p", PS)
def test_general_rule(p):
    """GENERAL_FORM.md: start at 2^p - 1, add d(t) = A006519(t) + A006519(A000265(t)+1)/2 - 1."""
    def low(x):                      # A006519: largest power of 2 dividing x
        return x & -x
    s, x = [], (1 << p) - 1
    while x < 1 << BITS:
        s.append(x)
        odd = x // low(x)            # A000265: odd part of x
        x += low(x) + low(odd + 1) // 2 - 1
    assert s == brute(p)


def test_known_values():
    # three 1s: the sequence from the workbook
    assert [difference(x) for x in islice(sequence(3), 10)] == [7, 4, 2, 1, 5, 2, 1, 3, 1, 2]
    assert build_group_differences(4, 3) == [5, 2, 1, 3, 1, 2]        # group 31
    assert build_group_differences(5, 4) == [9, 4, 2, 1, 5, 2, 1, 3, 1, 2]  # four 1s, group 63
    # Book1 Sheet7, group 63: a+2, b, c, d, e, f | d+2, e, f | f+2
    assert build_group_differences_blocks(5, 3) == [7, 2, 1, 3, 1, 2, 5, 1, 2, 4]

# Numbers with exactly k ones in binary, built from their differences

Ashwin Shashikant Niwalkar

For any k, the numbers whose binary form contains exactly k ones can be listed
in increasing order with one rule: start at 2^k - 1 and keep adding a
difference computed from the current number. The difference formula is the
same for every k. This note states the rule, proves it, and describes the
patterns inside the difference sequences.

## 1. The sequences

| k | Numbers with k ones in binary | OEIS |
|---|---|---|
| 1 | 1, 2, 4, 8, 16, 32, ... | [A000079](https://oeis.org/A000079) |
| 2 | 3, 5, 6, 9, 10, 12, 17, ... | [A018900](https://oeis.org/A018900) |
| 3 | 7, 11, 13, 14, 19, 21, 22, ... | [A014311](https://oeis.org/A014311) |
| 4 | 15, 23, 27, 29, 30, 39, 43, ... | [A014312](https://oeis.org/A014312) |
| 5 | 31, 47, 55, 59, 61, 62, 79, ... | [A014313](https://oeis.org/A014313) |
| 6 | 63, 95, 111, 119, 123, 125, ... | [A023688](https://oeis.org/A023688) |

Every sequence starts at 2^k - 1, the number with its k ones packed together
(1, 11, 111, 1111, ...).

## 2. The general rule

Let t be any positive number. Write

- **A006519(t)** for the largest power of 2 that divides t (in binary, the
  lowest 1 bit of t), and
- **A000265(t)** for the odd part of t (t with its trailing zeros removed).

Then the next number above t with the same number of ones is t + d(t), where

```
d(t) = A006519(t) + A006519(A000265(t) + 1)/2 - 1
```

So the numbers with k ones are

```
x(1) = 2^k - 1,    x(n+1) = x(n) + d(x(n)).
```

k appears only in the starting value. The difference d(t) depends only on t.

**Example, k = 4:**

| t | binary | A006519(t) | A000265(t) + 1 | d(t) | next |
|---|---|---|---|---|---|
| 15 | 1111 | 1 | 16 | 1 + 8 - 1 = 8 | 23 |
| 23 | 10111 | 1 | 24 | 1 + 4 - 1 = 4 | 27 |
| 27 | 11011 | 1 | 28 | 1 + 2 - 1 = 2 | 29 |
| 29 | 11101 | 1 | 30 | 1 + 1 - 1 = 1 | 30 |
| 30 | 11110 | 2 | 16 | 2 + 8 - 1 = 9 | 39 |

Starting the list from 0 instead gives a simpler statement: the k ones
sequence is the running total (partial sums) of 2^k - 1, d(x(1)), d(x(2)), ...
The 0 is only a starting point; it has no ones and is not in the sequence.

### Why it works

Write t in binary. It ends in v zeros. Above them is a run of w ones (bits v
to v+w-1), and bit v+w is 0. To get the next larger number with the same
number of ones:

1. move the top 1 of that run up one place, to bit v+w, and
2. move the other w-1 ones of the run down to the bottom, bits 0 to w-2.

Any smaller increase would have to change only bits below v+w, and the run
already sits as high as it can there. The run was worth 2^(v+w) - 2^v and is
replaced by 2^(v+w) + 2^(w-1) - 1, so

```
d(t) = 2^v + 2^(w-1) - 1.
```

Here 2^v = A006519(t). The odd part A000265(t) ends in exactly w ones, so
A000265(t) + 1 is divisible by 2^w but not by 2^(w+1). That means
A006519(A000265(t) + 1) = 2^w, and 2^(w-1) = A006519(A000265(t) + 1)/2.

Example: t = 30 = 11110. v = 1 and w = 4, so d = 2 + 8 - 1 = 9, and
30 + 9 = 39 = 100111.

### Checked by computer

For k = 1 to 6, building the sequence with this rule from 2^k - 1 gave
exactly the numbers below 2^20 with k ones, checked against a direct count.
There were C(20, k) of them in each case: 20, 190, 1140, 4845, 15504 and
38760.

## 3. The difference sequences

| k | Differences d(x(n)) | OEIS |
|---|---|---|
| 2 | 2, 1, 3, 1, 2, 5, 1, 2, 4, 9, ... | [A401546](https://oeis.org/A401546) |
| 3 | 4, 2, 1, 5, 2, 1, 3, 1, 2, 7, ... | [A228132](https://oeis.org/A228132) |
| 4 | 8, 4, 2, 1, 9, 4, 2, 1, 5, 2, ... | A401010 (submitted Nov 10 2026, under review) |
| 5 | 16, 8, 4, 2, 1, 17, 8, 4, 2, 1, ... | not in the OEIS (Nov 11 2026) |

The k ones sequence is rebuilt from its differences by starting at 2^k - 1
and adding them one at a time.

### Groups

Split the numbers with k ones by their highest bit. Group i holds the numbers
from 2^i to 2^(i+1) - 1 (labelled 15, 31, 63, ... in the workbooks), and
each number's difference is the gap from the number before it. For k ones and
i >= k:

- **Size:** C(i, k-1), because the top bit is fixed and the other k-1 ones
  can go in any of the i places below it. These are the diagonals of Pascal's
  triangle: 1, 2, 3, 4, ... (k = 2), 1, 3, 6, 10, ... (k = 3), 1, 4, 10,
  20, ... (k = 4).
- **Sum of the differences:** (2^k - 1) * 2^(i-k), which doubles from one
  group to the next.
- **Last difference:** 2^(i-k).

### The group rule (from the k-1 ones sequence)

Each group's differences come from the group before it:

1. add the increment 2^(i-k) to the first difference,
2. copy the rest of the previous group's differences,
3. append the differences of the matching group of the **k-1 ones**
   sequence.

Example, k = 3. Group 31 (numbers 16 to 31) has differences 5, 2, 1, 3, 1, 2.
Group 63 is

```
[5 + 2], 2, 1, 3, 1, 2   +   5, 1, 2, 4   =   7, 2, 1, 3, 1, 2, 5, 1, 2, 4
                             (two ones, group 31)
```

Why: hide the top 1 of a number with k ones and you have a number with k-1
ones. Copying keeps the old k-1 ones numbers under a higher top bit, so their
gaps are unchanged. The appended part is the k-1 ones numbers that only fit
under the new top bit.

The same rule builds two ones from one one, so starting from the powers of 2
it builds every k in turn.

### The block rule (from the previous group only)

The same groups can be built without the k-1 ones sequence. Cut the previous
group into k pieces at fixed starting places ("keys"). Each piece runs from
its key to the end of the group. Add the increment to the first number of
each piece, then place the pieces side by side. The places where the new
pieces start are the keys for the next group.

Example, k = 3. Group 31 = 5, 2, 1, 3, 1, 2, with keys at the 1st, 4th and
6th places:

```
5+2, 2, 1, 3, 1, 2  |  3+2, 1, 2  |  2+2
 7   2  1  3  1  2  |   5   1  2  |   4
```

The first group (i = k) is 2^(k-1), ..., 4, 2, 1, with a key at every place.

Why: piece j holds the numbers whose top j ones sit together (10xxxx,
110xxx, 1110xx, ...). A piece is the old tail with a 0 put in after the top
j ones, so the gaps inside it stay the same. Only the first gap of each piece
changes.

## 4. What is known and what is new

Known before this work:

- The "next number with the same number of ones" step is a classic
  programming trick known as Gosper's hack (HAKMEM, MIT AI Memo 239, 1972,
  item 175). D. E. Knuth covers it in *The Art of Computer Programming*,
  Vol. 4A, Section 7.1.3. The OEIS has it as
  [A057168](https://oeis.org/A057168).
- The OEIS formula a(n+1) = A057168(a(n)) for A014312 (M. F. Hasler, 2014).
- Group sizes C(i, k-1) are standard counting.

Contributed here:

- The difference formula written with A006519 and A000265, published in
  A057168 (Nov 10 2026) and A228132 (Nov 4 2026).
- The group rule and the block rule for the difference sequences. They come
  from my spreadsheet work, kept in this repository: `book1.txt` lists the
  three ones differences, and the block rule is in `Book1.xlsx` (file
  properties: created December 2012, last saved February 2018). An OEIS
  search on Oct 28 2026 found no record of either rule.
- The observation that one difference rule, started at 2^k - 1, gives every
  numbers with k ones sequence.

## 5. Timeline

| Date | Event |
|---|---|
| Dec 2012 | `Book1.xlsx` created; spreadsheet work on the three ones differences |
| Feb 2018 | `Book1.xlsx` last saved; it contains the block rule |
| Nov 2013 | OEIS A228132 (differences of A014311) created by another contributor |
| Nov 4 2026 | My formula and program added to A228132 |
| Nov 10 2026 | My formula published in A057168 |
| Nov 10 2026 | Differences of A014312 submitted as A401010 |

## 6. Check it yourself

The code in this repository checks every statement above against a direct
count, for k = 1 to 6 and all numbers below 2^16:

```
pip install -r requirements.txt
pytest
python ones_sequence.py -p 3 -b 6      # three ones, groups up to 6 bits
```

`ones_sequence.py` calls the number of ones p, not k.
`build_group_differences` is the group rule, and
`build_group_differences_blocks` is the block rule.

---

*Drafted with help from Claude (Anthropic) from my notes and code. Every
formula and example was checked by the tests in this repository.*

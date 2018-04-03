# paired

Paired is a Python package for pairwise alignment of arbitrary sequences. 

Python has lots of great packages for sequence alignment and time warping, but mostly for biological or numerical data. Paired performs global alignment on lists of arbitrary Python objects, and lets you define how element pairs are matched and scored.


## Basic usage

```python
import paired

seq_1 = 'The quick brown fox jumped over the lazy dog'.split(' ')
seq_2 = 'The brown fox leaped over the lazy dog'.split(' ')
alignment = paired.align(seq_1, seq_2)

print(alignment)
# [(0, 0), (1, None), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)]

for i_1, i_2 in alignment:
    print((seq_1[i_1] if i_1 is not None else '').ljust(15), end='')
    print(seq_2[i_2] if i_2 is not None else '')

# The            The
# quick          
# brown          brown
# fox            fox
# jumped         leaped
# over           over
# the            the
# lazy           lazy
# dog            dog
```



## Custom scores

Paired uses the [Needleman-Wunsch algorithm](https://en.wikipedia.org/wiki/Needleman%E2%80%93Wunsch_algorithm).  The scoring for the different operations (match, mismatch, gap) can be specified:

```python
alignment = paired.align(seq_1, seq_2, match_score=5, mismatch_score=-1, gap_score=-5)
```


## Custom similarity

By default, two elements are said to match if `element_1 == element_2`. Paired also allows you to pass a function to return a match/mismatch score for a given pair of elements. For example, you could give different scores to case-sensitive and case-insensitive matches of strings:


```python

def scorer(a, b):
    if a == b:
        return 2
    elif a.lower() == b.lower():
        return 1
    else:
        return -1

alignment = paired.align(seq_1, seq_2, scorer=scorer, gap_score=-3)
```




## Installation

Paired is on [PyPI](https://pypi.org/project/paired/) and can be installed with pip. It has no dependencies.

```shell
pip install paired
```


## API

`pairwise.align(x, y, match_score=1, mismatch_score=-1, gap_score=-1, scorer=None)`

Get the global alignment of two sequences.

Arguments:

* **x**, **y** (*list*): Sequences of objects to align.
* **match_score** (*numeric*): Score when matching elements are paired.
* **mismatch_score** (*numeric*): Score when mismatching elements are paired.
* **gap_score** (*numeric*): Score for an insertion/deletion, when an element is paired with no other element.
* **scorer** (*callable*): Function that takes two elements as inputs, and returns a numerical score based on how well they match.  If `None` is passed, the default function used is equivalent to `lambda a, b: match_score if a==b else mismatch_score`.

Returns: 

* **alignment** (*list of tuples*): The aligned sequence, as a list of pairs of indices into `x` and `y` respectively.  A gap is represented by `None` instead of an integer index.


## Running tests

Tests can be run with [pytest][https://docs.pytest.org/en/latest/]:

```shell
cd paired/
py.test
```
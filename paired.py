import itertools


__version__ = '0.0.1'


def _empty_2d_array(shape):
    '''
    Return a (list of rows) array of given shape, filled with zeros.

    Args:
        shape (tuple): A (n_rows, n_cols) tuple.

    Returns:
        a (list): Array of given shape filled with the same value. Can index with z[row][col].
    '''
    n_rows, n_cols = shape[0], shape[1]
    a = [[0 for _ in range(n_cols)] for _ in range(n_rows)]
    return a


def _make_standard_scorer(match_score, mismatch_score):
    '''
    Return a function that takes two elements and returns a score based on whether they are equal.

    Args:
        match_score (numeric): Score to return if elements are equal.
        mismatch_score (numeric): Score to return if elements are different.

    Returns:
        scorer (callable)
    '''
    def scorer(e_x, e_y):
        if e_x == e_y:
            return match_score
        else:
            return mismatch_score

    return scorer


def _similarity_matrix(x, y, scorer):
    '''
    Build matrix S where S[i][j] is the match/mismatch score of elements x[i] and y[j].

    Args:
        x, y (list): Sequences to be aligned.
        scorer (callable): Function that gives the match/mismatch score of two elements.

    Returns:
        s (array): Similarity matrix.
    '''
    n_x = len(x)
    n_y = len(y)
    s = _empty_2d_array((n_x, n_y))
    for i, j in itertools.product(range(n_x), range(n_y)):
        s[i][j] = scorer(x[i], y[j])

    return s


def _needleman_wunsch_forward_pass(n_x, n_y, s, gap_score):
    '''
    Compute the forward pass of the Needleman Wunsch algorithm.

    Args:
        n_x, n_y (int): The lengths of the sequences to be aligned.
        s (array): Match/mismatch similarity matrix.
        gap_score (numeric): Score for a insertion/deletion.

    Returns:
        f (array): Forward alignment matrix.
    '''

    # The alignment matrix is one larger than the length of each sequences,
    # cause the first row/col consists of gaps.
    f = _empty_2d_array((n_x + 1, n_y + 1))
    f[0] = [i * gap_score for i in range(n_y + 1)]

    # Then iterate over each column of each row, taking the best possible
    # score. The deletion scores for the entire row can be computed at once.
    for i_row in range(1, n_x + 1):
        deletions = [c + gap_score for c in f[i_row - 1]]
        f[i_row][0] = deletions[0]
        for i_col in range(1, n_y + 1):
            match = f[i_row - 1][i_col - 1] + s[i_row - 1][i_col - 1]
            delete = deletions[i_col]
            insert = f[i_row][i_col - 1] + gap_score
            f[i_row][i_col] = max(match, delete, insert)

    return f


def _needleman_wunsch_backward_pass(n_x, n_y, s, f, gap_score):
    '''
    Compute the backward pass of the Needleman Wunsch algorithm.

    Args:
        n_x, n_y (int): The lengths of the sequences to be aligned.
        s (array): Match/mismatch similarity matrix.
        f (array): Forward pass alignment matrix.
        gap_score (numeric): Score for a insertion/deletion.

    Returns:
        alignment (list of tuples): The aligned sequence, as a list of pairs of indices.
    '''

    alignment = []
    i = n_x
    j = n_y
    while i > 0 or j > 0:
        if i > 0 and j > 0 and f[i][j] == f[i - 1][j - 1] + s[i - 1][j - 1]:
            alignment.append((i - 1, j - 1))
            i = i - 1
            j = j - 1
        elif i > 0 and f[i][j] == f[i - 1][j] + gap_score:
            alignment.append((i - 1, None))
            i = i - 1
        else:
            alignment.append((None, j - 1))
            j = j - 1

    alignment = alignment[::-1]
    return alignment


def align(x, y, match_score=1, mismatch_score=-1, gap_score=-3, scorer=None):
    '''

    Get the global alignment of two sequences.

    Args:
        x, y (list): Sequences of objects to align.
        match_score (numeric): Score when matching elements are paired.
        mismatch_score (numeric): Score when mismatching elements are paired.
        gap_score (numeric): Score for an insertion/deletion, when an element is paired with no other
            element.
        scorer (callable): Function that takes two elements as inputs, and returns a numerical 
            score based on how well they match.  If `None` is passed, the default function used is
            equivalent to `lamdba a, b: match_score if a==b else mismatch_score`.

    Returns: 
        alignment (list of tuples): The aligned sequence, as a list of pairs of indices into `x` and `y`
            respectively.  A gap is represented by `None` instead of an integer index.
    '''

    if scorer is None:
        scorer = _make_standard_scorer(match_score, mismatch_score)

    n_x = len(x)
    n_y = len(y)
    s = _similarity_matrix(x, y, scorer)
    f = _needleman_wunsch_forward_pass(n_x, n_y, s, gap_score)
    alignment = _needleman_wunsch_backward_pass(n_x, n_y, s, f, gap_score)

    return alignment

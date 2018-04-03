import paired


class TestEmpty2DArray(object):
    def test_shape(self):
        shape = (2, 3)
        arr = paired._empty_2d_array(shape)
        assert len(arr) == shape[0]
        assert len(arr[0]) == shape[1]

    def test_rows_are_different_objects(self):
        arr = paired._empty_2d_array((2, 2))
        assert arr[0] == arr[1]
        assert arr[0] is not arr[1]


class TestMakeStandardScorer(object):
    def setup_class(self):
        self.match_score = 1
        self.mismatch_score = -1
        scorer = paired._make_standard_scorer(
            self.match_score, self.mismatch_score)
        self.scorer = staticmethod(scorer)  # Avoid creating a bound method.

    def test_match_score(self):
        assert self.scorer('same', 'same') == self.match_score

    def test_mismatch_score(self):
        assert self.scorer('not', 'same') == self.mismatch_score

    def test_standard_scorer_matches_documentation(self):
        doc_scorer = lambda a, b: self.match_score if a == b else self.mismatch_score
        assert self.scorer('same', 'same') == doc_scorer('same', 'same')
        assert self.scorer('not', 'same') == doc_scorer('not', 'same')


class TestAlign(object):
    def test_readme_example(self):
        x = 'The quick brown fox jumped over the lazy dog'.split(' ')
        y = 'The brown fox leaped over the lazy dog'.split(' ')
        alignment = paired.align(x, y)
        assert alignment == [(0, 0), (1, None), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (7, 6), (8, 7)]

    def test_gaps_in_both_sequences(self):
        x = 'The quick brown fox jumped over the lazy dog'.split(' ')
        y = 'The brown fox leaped over the extremely lazy dog'.split(' ')
        alignment = paired.align(x, y)
        assert alignment == [(0, 0), (1, None), (2, 1), (3, 2), (4, 3), (5, 4), (6, 5), (None, 6), (7, 7), (8, 8)]

    def test_identical_sequences(self):
        x = list(range(100))
        y = list(x)
        alignment = paired.align(x, y)
        assert alignment == [(i, i) for i in range(len(x))]

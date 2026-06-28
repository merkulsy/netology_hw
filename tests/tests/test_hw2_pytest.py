import pytest
from hw2 import vote

class TestVote:
    @pytest.mark.parametrize(
        "votes, expected",
        [
            ([1, 1, 1, 2, 3], 1),
            ([1, 2, 3, 2, 2], 2),
            ([5, 5, 5, 5], 5),
            ([1, 2, 3, 4], 1),
            ([10, 20, 30, 10, 10], 10),
            ([7, 7, 8, 8, 8], 8),
        ]
    )
    def test_vote(self, votes, expected):
        assert vote(votes) == expected
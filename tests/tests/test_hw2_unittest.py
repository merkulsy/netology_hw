import unittest
from hw2 import vote

class TestVote(unittest.TestCase):
    def test_vote(self):
        params = (
            ([1, 1, 1, 2, 3], 1),
            ([1, 2, 3, 2, 2], 2),
            ([5, 5, 5, 5], 5),
            ([10, 20, 30, 10, 10], 10),
            ([7, 7, 8, 8, 8], 8),
        )
        for votes, expected in params:
            with self.subTest(votes=votes):
                self.assertEqual(vote(votes), expected)
import pytest
from hw1 import solution

class TestQuadratic:
    @pytest.mark.parametrize(
        "a, b, c, expected_output",
        [
            (1, 8, 15, (-3.0, -5.0)),   # два корня
            (1, -13, 12, (12.0, 1.0)),  # два корня
            (-4, 28, -49, 3.5),         # один корень
            (1, 1, 1, "корней нет"),    # корней нет
        ]
    )
    def test_solution(self, a, b, c, expected_output):
        assert solution(a, b, c) == expected_output
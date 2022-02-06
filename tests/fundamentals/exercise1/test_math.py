from unittest import TestCase
from parameterized import parameterized

from src.mytest.fundamentals.exercise1.math import Math


class TestMath(TestCase):
    def setUp(self) -> None:
        self.math = Math()

    def test_add_when_called_return_the_sum_of_arguments(self):
        result = self.math.add(1, 2)
        self.assertEqual(3, result)

    @parameterized.expand([(1, 2, 2), (3, 1, 3), (4, 4, 4)])
    def test_max_when_called_return_the_max_of_arguments(self, a, b, expectedValue):
        result = self.math.max(a, b)
        self.assertEqual(expectedValue, result)

    def test_get_odd_numbers(self):
        result = self.math.get_odd_numbers(5)
        self.assertEqual([1, 3, 5], list(result))

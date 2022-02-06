from unittest import TestCase

from src.mytest.fundamentals.exercise0.reservation import Reservation, User


class TestReservation(TestCase):

    def setUp(self) -> None:
        # Arrange
        self.user = User()
        self.reservation = Reservation(user=self.user)

    def test_can_be_cancelled_by_admin_user_cancelling_return_true(self):
        # Act
        result = self.reservation.can_be_cancelled_by(User(True))

        # Assert
        self.assertTrue(result)

    def test_can_be_cancelled_by_same_user_cancelling_return_true(self):
        # Act
        result = self.reservation.can_be_cancelled_by(self.user)

        # Assert
        self.assertTrue(result)

    def test_can_be_cancelled_by_another_user_cancelling_return_true(self):
        # Act
        user = User();
        result = self.reservation.can_be_cancelled_by(user)

        # Assert
        self.assertFalse(result)

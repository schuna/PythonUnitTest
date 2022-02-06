class Reservation:
    def __init__(self, user):
        self.made_by = user

    def can_be_cancelled_by(self, user):
        return user.is_admin or self.made_by is user


class User:
    def __init__(self, is_admin=False):
        self.is_admin = is_admin

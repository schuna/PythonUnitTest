class Math:
    def __init__(self):
        pass

    @staticmethod
    def add(a, b):
        return a + b

    @staticmethod
    def max(a, b):
        if a > b:
            return a
        return b

    @staticmethod
    def get_odd_numbers(limit):
        for i in range(limit + 1):
            if i % 2 != 0:
                yield i

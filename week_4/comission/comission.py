class Value:
    def __init__(self):
        self.amount = None

    def __get__(self, obj, obj_type):
        return self.amount

    def __set__(self, obj, value):
        if hasattr(obj, 'commission'):
            value *= 1. - obj.commission
        self.amount = value


class Account:
    amount = Value()

    def __init__(self, commission):
        self.commission = commission


if __name__ == '__main__':
    new_account = Account(0.1)
    new_account.amount = 100
    print(new_account.amount)



def maximum_100_usd_total(func):
    def wrapper_max(orders):
        total = func(orders)
        if total > 100:
            raise RuleViolationException("Total more than 100")
        return total
    return wrapper_max


def discount_of_1_usd_above_20(func):
    def wrapper_one_over_twenty(orders):
        total = func(orders)
        if total >= 20:
            total = total - 1
        return total
    return wrapper_one_over_twenty


def every_fifth_free(func):
    def wrapper_fifth_free(orders: dict):
        for _, order in orders.items():
            if order["amount"] >= 5:
                order["amount"] -= order["amount"]/5
        return func(orders)
    return wrapper_fifth_free


class RuleViolationException(BaseException):
    pass

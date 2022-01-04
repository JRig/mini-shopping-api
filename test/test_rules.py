from test.test_product_validation import \
    TEST_PRODUCT, TEST_PRODUCT2,\
    TEST_PRODUCT3, TEST_PRODUCT4,\
    TEST_PRODUCT5
from src.cart_handler import base_calculation
from src.rules import \
    RuleViolationException,\
    discount_of_1_usd_above_20,\
    maximum_100_usd_total,\
    every_fifth_free


def test_can_calculate_5_products_discount():
    orders = {
        "1": {
            "price": 20,
            "amount": 5
        }
    }
    expected_total = 80

    @every_fifth_free
    def test_calculate_total(orders):
        return base_calculation(orders)

    actual_total = test_calculate_total(orders)

    assert actual_total == expected_total


def test_total_amount_no_higher_than_100_usd():
    orders = {
        "1": {
            "price": 101,
            "amount": 1
        }
    }

    @maximum_100_usd_total
    def test_calculate_total(orders):
        return base_calculation(orders)

    try:
        test_calculate_total(orders)
        assert False, "No error raised"
    except RuleViolationException:
        assert True


def test_can_add_1_usd_discount_on_large_purchases():
    orders = {
        "1": {
            "price": 21,
            "amount": 1
        }
    }
    expected_total = 20

    @discount_of_1_usd_above_20
    def test_calculate_total(orders):
        return base_calculation(orders)

    actual_total = test_calculate_total(orders)

    assert actual_total == expected_total


def test_can_add_three_rules():
    orders = {
        "1": {
            "price": 21,
            "amount": 5
        }
    }
    expected_total = 83

    @every_fifth_free
    @maximum_100_usd_total
    @discount_of_1_usd_above_20
    def test_calculate_total(orders):
        return base_calculation(orders)

    actual_total = test_calculate_total(orders)

    assert actual_total == expected_total

    orders = {
        "1": {
            "price": 21,
            "amount": 6
        }
    }

    try:
        gt_100_total = test_calculate_total(orders)
        assert False, f"Total {gt_100_total} should be > 100"
    except RuleViolationException:
        assert True

    assert actual_total == expected_total

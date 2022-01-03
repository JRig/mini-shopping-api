from src.validations import validate_product

TEST_PRODUCT = {
        "title": "Product1",
        "description": "My description",
        "price": 20,
        "currency": "USD",
        "stock": 1
    }

TEST_PRODUCT2 = {
        "title": "Product2",
        "description": "My description2",
        "price": 22,
        "currency": "USD",
        "stock": 1
    }

TEST_PRODUCT3 = {
        "title": "Product3",
        "description": "My description3",
        "price": 15,
        "currency": "USD",
        "stock": 4
    }

TEST_PRODUCT4 = {
        "title": "Product4",
        "description": "My description4",
        "price": 50,
        "currency": "USD",
        "stock": 2
    }

TEST_PRODUCT5 = {
        "title": "Product5",
        "description": "My description5",
        "price": 5,
        "currency": "USD",
        "stock": 5
    }


def test_valid_product_validates():
    valid_product = TEST_PRODUCT
    assert validate_product(valid_product)


def test_invalid_product_does_not_validate():
    invalid_product = {
        "titel": "Product2",
        "description": [""],
        "value": 22,
        "currency": "USD"
    }
    validated, err_msg = validate_product(invalid_product)
    print(err_msg)
    assert not validated

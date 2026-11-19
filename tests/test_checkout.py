import pytest

from data.test_data import CUSTOMER, PRODUCTS


def _checkout_info(login_as, *product_keys):
    inventory = login_as()
    for key in product_keys:
        inventory.add_to_cart(PRODUCTS[key][0])
    return inventory.open_cart().checkout()


@pytest.mark.smoke
def test_end_to_end_purchase(login_as):
    overview = _checkout_info(login_as, "backpack", "bike_light").fill(**CUSTOMER).continue_to_overview()

    expected_subtotal = PRODUCTS["backpack"][2] + PRODUCTS["bike_light"][2]
    assert overview.subtotal() == pytest.approx(expected_subtotal)
    assert overview.total() == pytest.approx(overview.subtotal() + overview.tax())

    complete = overview.finish()
    assert complete.header() == "Thank you for your order!"
    assert complete.cart_count() == 0


@pytest.mark.regression
@pytest.mark.parametrize("field, expected_error", [
    ("first_name", "Error: First Name is required"),
    ("last_name", "Error: Last Name is required"),
    ("postal_code", "Error: Postal Code is required"),
])
def test_checkout_requires_every_field(login_as, field, expected_error):
    info = _checkout_info(login_as, "backpack")
    data = {**CUSTOMER, field: ""}
    info.fill(**data).submit()
    assert info.error_message() == expected_error


@pytest.mark.regression
def test_tax_is_eight_percent(login_as):
    overview = _checkout_info(login_as, "fleece_jacket").fill(**CUSTOMER).continue_to_overview()
    assert overview.tax() == pytest.approx(round(overview.subtotal() * 0.08, 2))

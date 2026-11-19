import pytest

from data.test_data import PRODUCTS


@pytest.mark.smoke
def test_cart_shows_added_products(login_as):
    inventory = login_as()
    for key in ("backpack", "onesie"):
        inventory.add_to_cart(PRODUCTS[key][0])

    cart = inventory.open_cart()
    assert sorted(cart.item_names()) == sorted([PRODUCTS["backpack"][1], PRODUCTS["onesie"][1]])


@pytest.mark.regression
def test_remove_from_cart_page(login_as):
    inventory = login_as().add_to_cart(PRODUCTS["backpack"][0])
    cart = inventory.open_cart().remove(PRODUCTS["backpack"][0])
    assert cart.item_names() == []
    assert cart.cart_count() == 0


@pytest.mark.regression
def test_cart_persists_after_continue_shopping(login_as):
    inventory = login_as().add_to_cart(PRODUCTS["bike_light"][0])
    inventory = inventory.open_cart().continue_shopping()
    assert inventory.cart_count() == 1

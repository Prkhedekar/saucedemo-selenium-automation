import pytest

from data.test_data import PRODUCTS


@pytest.mark.regression
@pytest.mark.parametrize("option", ["name_asc", "name_desc"])
def test_sort_by_name(login_as, option):
    inventory = login_as().sort_by(option)
    names = inventory.item_names()
    assert names == sorted(names, reverse=(option == "name_desc"))


@pytest.mark.regression
@pytest.mark.parametrize("option", ["price_asc", "price_desc"])
def test_sort_by_price(login_as, option):
    inventory = login_as().sort_by(option)
    prices = inventory.item_prices()
    assert prices == sorted(prices, reverse=(option == "price_desc"))


@pytest.mark.smoke
def test_inventory_lists_six_products(login_as):
    assert len(login_as().item_names()) == 6


@pytest.mark.smoke
def test_add_and_remove_updates_cart_badge(login_as):
    backpack, _, _ = PRODUCTS["backpack"]
    bike_light, _, _ = PRODUCTS["bike_light"]
    inventory = login_as()

    inventory.add_to_cart(backpack).add_to_cart(bike_light)
    assert inventory.cart_count() == 2

    inventory.remove_from_cart(backpack)
    assert inventory.cart_count() == 1

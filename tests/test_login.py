import pytest

from data.test_data import INVALID_LOGINS, PASSWORD, STANDARD_USER
from pages.login_page import LoginPage


@pytest.mark.smoke
def test_valid_login_opens_inventory(driver):
    inventory = LoginPage(driver).open().login(STANDARD_USER, PASSWORD)
    assert inventory.title() == "Products"
    assert driver.current_url.endswith("/inventory.html")


@pytest.mark.regression
@pytest.mark.parametrize("username, password, expected_error", INVALID_LOGINS,
                         ids=["both-empty", "no-password", "no-username", "wrong-password",
                              "unknown-user", "locked-out-user"])
def test_invalid_login_shows_error(driver, username, password, expected_error):
    login = LoginPage(driver).open()
    login.submit(username, password)
    assert login.error_message() == expected_error
    assert login.is_displayed(), "user should stay on the login page"


@pytest.mark.smoke
def test_logout_returns_to_login(login_as):
    login = login_as().logout()
    assert login.is_displayed()


@pytest.mark.regression
def test_inventory_blocked_without_login(driver):
    driver.get("https://www.saucedemo.com/inventory.html")
    login = LoginPage(driver)
    assert "You can only access '/inventory.html' when you are logged in." in login.error_message()

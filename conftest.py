"""Shared fixtures: browser setup, logged-in sessions, and screenshots attached to the HTML report on failure."""

import pytest
from selenium import webdriver

from data.test_data import PASSWORD, STANDARD_USER
from pages.login_page import LoginPage


def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default="chrome", choices=["chrome", "firefox", "edge"])
    parser.addoption("--headless", action="store_true", help="run the browser without a window (used in CI)")


def _build_driver(browser: str, headless: bool):
    if browser == "chrome":
        options = webdriver.ChromeOptions()
        # Stop Chrome's password-manager popups from covering the page after login.
        options.add_experimental_option("prefs", {
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False,
            "profile.password_manager_leak_detection": False,
        })
        options.add_argument("--window-size=1280,900")
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Chrome(options=options)
    if browser == "edge":
        options = webdriver.EdgeOptions()
        options.add_argument("--window-size=1280,900")
        if headless:
            options.add_argument("--headless=new")
        return webdriver.Edge(options=options)
    options = webdriver.FirefoxOptions()
    if headless:
        options.add_argument("-headless")
    driver = webdriver.Firefox(options=options)
    driver.set_window_size(1280, 900)
    return driver


@pytest.fixture
def driver(request):
    driver = _build_driver(request.config.getoption("--browser"), request.config.getoption("--headless"))
    yield driver
    driver.quit()


@pytest.fixture
def login_as(driver):
    """Log in as the given user and return the inventory page."""
    def _login(username: str = STANDARD_USER, password: str = PASSWORD):
        return LoginPage(driver).open().login(username, password)
    return _login


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """Attach a screenshot to the HTML report when a test fails."""
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return
    driver = item.funcargs.get("driver")
    if driver is None:
        return
    pytest_html = item.config.pluginmanager.getplugin("html")
    if pytest_html is None:
        return
    screenshot = driver.get_screenshot_as_base64()
    extras = getattr(report, "extras", [])
    extras.append(pytest_html.extras.image(screenshot, "Screenshot on failure"))
    extras.append(pytest_html.extras.url(driver.current_url, "Page URL"))
    report.extras = extras

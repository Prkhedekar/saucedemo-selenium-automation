from selenium.webdriver.common.by import By

from data.test_data import BASE_URL
from pages.base_page import BasePage


class LoginPage(BasePage):
    USERNAME = (By.ID, "user-name")
    PASSWORD = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> "LoginPage":
        self.driver.get(BASE_URL)
        self.find(self.LOGIN_BUTTON)
        return self

    def submit(self, username: str, password: str) -> None:
        self.type(self.USERNAME, username)
        self.type(self.PASSWORD, password)
        self.click(self.LOGIN_BUTTON)

    def login(self, username: str, password: str):
        """Log in and return the inventory page. Use submit() for logins that are expected to fail."""
        from pages.inventory_page import InventoryPage
        self.submit(username, password)
        return InventoryPage(self.driver).wait_until_loaded()

    def error_message(self) -> str:
        return self.text_of(self.ERROR)

    def is_displayed(self) -> bool:
        return self.is_present(self.LOGIN_BUTTON)

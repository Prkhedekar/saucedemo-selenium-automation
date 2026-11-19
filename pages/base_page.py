"""Common actions every page object uses. All interactions go through explicit waits, never time.sleep."""

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

Locator = tuple[str, str]


class BasePage:
    TIMEOUT = 10

    CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")

    def __init__(self, driver: WebDriver):
        self.driver = driver
        self.wait = WebDriverWait(driver, self.TIMEOUT)

    def find(self, locator: Locator) -> WebElement:
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_all(self, locator: Locator) -> list[WebElement]:
        self.wait.until(EC.presence_of_all_elements_located(locator))
        return self.driver.find_elements(*locator)

    def click(self, locator: Locator) -> None:
        self.wait.until(EC.element_to_be_clickable(locator)).click()

    def type(self, locator: Locator, text: str) -> None:
        field = self.find(locator)
        field.clear()
        field.send_keys(text)

    def text_of(self, locator: Locator) -> str:
        return self.find(locator).text

    def is_present(self, locator: Locator) -> bool:
        return len(self.driver.find_elements(*locator)) > 0

    # Header actions available on every page after login
    def cart_count(self) -> int:
        badges = self.driver.find_elements(*self.CART_BADGE)
        return int(badges[0].text) if badges else 0

    def open_cart(self):
        from pages.cart_page import CartPage
        self.click(self.CART_LINK)
        return CartPage(self.driver)

    def logout(self):
        from pages.login_page import LoginPage
        self.click(self.MENU_BUTTON)
        self.click(self.LOGOUT_LINK)
        return LoginPage(self.driver)

"""The three checkout steps: your information, overview, and order complete."""

import re

from selenium.webdriver.common.by import By

from pages.base_page import BasePage


class CheckoutInfoPage(BasePage):
    FIRST_NAME = (By.ID, "first-name")
    LAST_NAME = (By.ID, "last-name")
    POSTAL_CODE = (By.ID, "postal-code")
    CONTINUE = (By.ID, "continue")
    ERROR = (By.CSS_SELECTOR, "[data-test='error']")

    def fill(self, first_name: str, last_name: str, postal_code: str) -> "CheckoutInfoPage":
        self.type(self.FIRST_NAME, first_name)
        self.type(self.LAST_NAME, last_name)
        self.type(self.POSTAL_CODE, postal_code)
        return self

    def field_values(self) -> dict[str, str]:
        return {
            "first_name": self.find(self.FIRST_NAME).get_attribute("value"),
            "last_name": self.find(self.LAST_NAME).get_attribute("value"),
            "postal_code": self.find(self.POSTAL_CODE).get_attribute("value"),
        }

    def submit(self) -> None:
        self.click(self.CONTINUE)

    def continue_to_overview(self) -> "CheckoutOverviewPage":
        self.submit()
        return CheckoutOverviewPage(self.driver)

    def error_message(self) -> str:
        return self.text_of(self.ERROR)


class CheckoutOverviewPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    SUBTOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    TAX = (By.CLASS_NAME, "summary_tax_label")
    TOTAL = (By.CLASS_NAME, "summary_total_label")
    FINISH = (By.ID, "finish")

    def item_names(self) -> list[str]:
        self.find(self.FINISH)
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def subtotal_text(self) -> str:
        return self.text_of(self.SUBTOTAL)

    @staticmethod
    def _amount(label: str) -> float:
        return float(re.search(r"\$([\d.]+)", label).group(1))

    def subtotal(self) -> float:
        return self._amount(self.subtotal_text())

    def tax(self) -> float:
        return self._amount(self.text_of(self.TAX))

    def total(self) -> float:
        return self._amount(self.text_of(self.TOTAL))

    def finish(self) -> "CheckoutCompletePage":
        self.click(self.FINISH)
        return CheckoutCompletePage(self.driver)


class CheckoutCompletePage(BasePage):
    HEADER = (By.CLASS_NAME, "complete-header")

    def header(self) -> str:
        return self.text_of(self.HEADER)

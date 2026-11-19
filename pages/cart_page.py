from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from pages.base_page import BasePage


class CartPage(BasePage):
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    CHECKOUT_BUTTON = (By.ID, "checkout")
    CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def item_names(self) -> list[str]:
        self.find(self.CHECKOUT_BUTTON)  # page loaded
        return [e.text for e in self.driver.find_elements(*self.ITEM_NAMES)]

    def remove(self, product_id: str) -> "CartPage":
        button = (By.ID, f"remove-{product_id}")
        self.click(button)
        # The cart re-renders after a removal; wait for the row to go before reading the page again.
        self.wait.until(EC.invisibility_of_element_located(button))
        return self

    def checkout(self):
        from pages.checkout_page import CheckoutInfoPage
        self.click(self.CHECKOUT_BUTTON)
        return CheckoutInfoPage(self.driver)

    def continue_shopping(self):
        from pages.inventory_page import InventoryPage
        self.click(self.CONTINUE_SHOPPING)
        return InventoryPage(self.driver).wait_until_loaded()

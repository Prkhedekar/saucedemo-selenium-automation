from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

from pages.base_page import BasePage


class InventoryPage(BasePage):
    TITLE = (By.CLASS_NAME, "title")
    ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    SORT_DROPDOWN = (By.CSS_SELECTOR, "[data-test='product-sort-container']")

    SORT_OPTIONS = {"name_asc": "az", "name_desc": "za", "price_asc": "lohi", "price_desc": "hilo"}

    def wait_until_loaded(self) -> "InventoryPage":
        self.find(self.TITLE)
        return self

    def title(self) -> str:
        return self.text_of(self.TITLE)

    def add_to_cart(self, product_id: str) -> "InventoryPage":
        self.click((By.ID, f"add-to-cart-{product_id}"))
        return self

    def remove_from_cart(self, product_id: str) -> "InventoryPage":
        self.click((By.ID, f"remove-{product_id}"))
        return self

    def item_names(self) -> list[str]:
        return [e.text for e in self.find_all(self.ITEM_NAMES)]

    def item_prices(self) -> list[float]:
        return [float(e.text.lstrip("$")) for e in self.find_all(self.ITEM_PRICES)]

    def sort_by(self, option: str) -> "InventoryPage":
        Select(self.find(self.SORT_DROPDOWN)).select_by_value(self.SORT_OPTIONS[option])
        return self

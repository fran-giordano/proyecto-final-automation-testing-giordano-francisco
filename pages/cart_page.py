from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class CartPage:
    _TITLE = (By.CLASS_NAME, "title")
    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _ITEM_PRICES = (By.CLASS_NAME, "inventory_item_price")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING_BUTTON = (By.ID, "continue-shopping")
    _REMOVE_BUTTONS = (By.CSS_SELECTOR, "button[data-test*='remove']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)
        self._verificar_pagina()

    def _verificar_pagina(self):
        """Verifica automáticamente que estamos en la página correcta."""
        self.wait.until(EC.visibility_of_element_located(self._TITLE))

    def obtener_titulo(self) -> str:
        return self.driver.find_element(*self._TITLE).text

    def obtener_productos(self) -> list:
        return self.driver.find_elements(*self._CART_ITEMS)

    def obtener_cantidad_productos(self) -> int:
        return len(self.driver.find_elements(*self._CART_ITEMS))

    def obtener_nombres_productos(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self._ITEM_NAMES)]

    def obtener_precios_productos(self) -> list[str]:
        return [el.text for el in self.driver.find_elements(*self._ITEM_PRICES)]

    def eliminar_producto_por_indice(self, indice: int = 0):
        botones = self.driver.find_elements(*self._REMOVE_BUTTONS)
        botones[indice].click()
        return self

    def ir_al_inventario(self):
        self.driver.find_element(*self._CONTINUE_SHOPPING_BUTTON).click()
        from pages.inventory_page import InventoryPage
        return InventoryPage(self.driver)

    def ir_al_checkout(self):
        self.driver.find_element(*self._CHECKOUT_BUTTON).click()
        return self
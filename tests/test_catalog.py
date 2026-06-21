import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestCatalogo:
    """Tests de funcionalidad del catálogo de productos."""

    def _login(self, driver, credenciales):
        """Helper privado para evitar duplicación de login."""
        LoginPage(driver).open().login(
            credenciales["username"], credenciales["password"]
        )
        return InventoryPage(driver)

    @pytest.mark.smoke
    @pytest.mark.catalog
    def test_titulo_inventario(self, driver, credenciales_validas):
        """Verifica que el título de la página sea 'Products'."""
        inventory_page = self._login(driver, credenciales_validas)
        assert inventory_page.obtener_titulo().text == "Products"

    @pytest.mark.catalog
    def test_productos_visibles(self, driver, credenciales_validas):
        """Verifica que haya al menos un producto en el catálogo."""
        inventory_page = self._login(driver, credenciales_validas)
        assert len(inventory_page.obtener_productos()) > 0

    @pytest.mark.catalog
    def test_primer_producto_valido(self, driver, credenciales_validas):
        """Verifica que el primer producto tenga nombre y precio válido."""
        inventory_page = self._login(driver, credenciales_validas)
        productos = inventory_page.obtener_productos()
        nombre = productos[0].find_element(By.CLASS_NAME, "inventory_item_name")
        precio = productos[0].find_element(By.CLASS_NAME, "inventory_item_price")
        assert nombre.text
        assert precio.text.startswith("$")
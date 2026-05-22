import pytest
from selenium.webdriver.common.by import By
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

class TestCarrito:
    """Tests de funcionalidad del carrito de compras."""

    def _login(self, driver, credenciales):
        """Helper privado para evitar duplicación de login."""
        LoginPage(driver).open().login_completo(
            credenciales["username"], credenciales["password"]
        )
        return InventoryPage(driver)

    @pytest.mark.smoke
    @pytest.mark.cart
    def test_agregar_producto_al_carrito(self, driver, credenciales_validas):
        """Verifica que un producto se agregue correctamente al carrito."""
        inventory_page = self._login(driver, credenciales_validas)
        productos = inventory_page.obtener_productos()
        nombre_esperado = productos[0].find_element(By.CLASS_NAME, "inventory_item_name").text
        inventory_page.agregar_al_carrito()
        assert inventory_page.obtener_contador_carrito() == 1
        cart_page = inventory_page.ir_al_carrito()
        assert cart_page.obtener_cantidad_productos() == 1
        assert nombre_esperado in cart_page.obtener_nombres_productos()

    @pytest.mark.cart
    def test_eliminar_producto_del_carrito(self, driver, credenciales_validas):
        """Verifica que un producto pueda eliminarse del carrito."""
        self._login(driver, credenciales_validas)
        InventoryPage(driver).agregar_al_carrito().ir_al_carrito().eliminar_producto_por_indice(0)
        assert CartPage(driver).obtener_cantidad_productos() == 0

    @pytest.mark.cart
    def test_continuar_comprando(self, driver, credenciales_validas):
        """Verifica que el botón continuar comprando regrese al inventario."""
        self._login(driver, credenciales_validas)
        InventoryPage(driver).agregar_al_carrito().ir_al_carrito().ir_al_inventario()
        assert "/inventory.html" in driver.current_url
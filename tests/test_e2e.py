import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage

class TestFlujoCompleto:
    """Tests de flujo completo end-to-end."""

    def _login(self, driver):
        """Helper con credenciales estándar para flujos E2E."""
        LoginPage(driver).open().usuario("standard_user").password("secret_sauce").click()
        return InventoryPage(driver)

    @pytest.mark.e2e
    @pytest.mark.regression
    def test_flujo_login_agregar_carrito_logout(self, driver):
        """Flujo completo: login → agregar producto → carrito → logout."""
        inventory_page = self._login(driver)
        inventory_page.agregar_al_carrito()
        assert inventory_page.obtener_contador_carrito() == 1
        cart_page = inventory_page.ir_al_carrito()
        assert cart_page.obtener_cantidad_productos() == 1
        inventory_page = cart_page.ir_al_inventario()
        inventory_page.cerrar_sesion()
        assert driver.current_url == "https://www.saucedemo.com/"

    @pytest.mark.e2e
    @pytest.mark.regression
    def test_flujo_agregar_y_eliminar(self, driver):
        """Flujo completo: agregar producto al carrito y eliminarlo."""
        inventory_page = self._login(driver)
        cart_page = inventory_page.agregar_al_carrito().ir_al_carrito()
        cart_page.eliminar_producto_por_indice(0)
        assert cart_page.obtener_cantidad_productos() == 0

    @pytest.mark.e2e
    def test_flujo_multiples_productos(self, driver):
        """Verifica que múltiples productos se agreguen correctamente."""
        inventory_page = self._login(driver)
        inventory_page.agregar_al_carrito()
        inventory_page.agregar_al_carrito()
        assert inventory_page.obtener_contador_carrito() == 2
        assert inventory_page.ir_al_carrito().obtener_cantidad_productos() == 2
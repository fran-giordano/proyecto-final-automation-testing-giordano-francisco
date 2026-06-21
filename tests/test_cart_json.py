import pytest
import pathlib
from utils.datos import leer_json_productos

BASE = pathlib.Path(__file__).parent.parent
PRODUCTOS = leer_json_productos(BASE / 'datos' / 'productos.json')

@pytest.fixture
def usuario_logueado(driver):
    """Fixture que realiza login antes de cada test de carrito"""
    from pages.login_page import LoginPage
    LoginPage(driver).open()
    LoginPage(driver).login("standard_user", "secret_sauce")
    return driver

@pytest.mark.parametrize("producto", PRODUCTOS)
def test_agregar_producto_desde_json(usuario_logueado, producto):
    """Test que agrega cada producto del JSON al carrito"""
    from pages.inventory_page import InventoryPage
    page = InventoryPage(usuario_logueado)
    page.add_to_cart(producto['nombre'])
    assert page.cart_count() >= 1, f"No se agregó: {producto['nombre']}"

@pytest.mark.smoke
def test_carrito_smoke(usuario_logueado):
    """Smoke: funcionalidad básica del carrito"""
    from pages.inventory_page import InventoryPage
    page = InventoryPage(usuario_logueado)
    page.add_to_cart(PRODUCTOS[0]['nombre'])
    assert page.cart_count() >= 1
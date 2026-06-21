import pytest
import pathlib
from utils.datos import leer_csv_login

BASE = pathlib.Path(__file__).parent.parent
CASOS_LOGIN = leer_csv_login(BASE / 'datos' / 'login.csv')

@pytest.mark.parametrize("usuario,clave,debe_funcionar,descripcion", CASOS_LOGIN)
def test_login_desde_csv(driver, usuario, clave, debe_funcionar, descripcion):
    """Test parametrizado que verifica el login con datos del CSV"""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    page.login(usuario, clave)
    if debe_funcionar:
        assert page.is_logged_in(), f"Falló login válido: {descripcion}"
    else:
        assert page.has_error(), f"Debió fallar pero no falló: {descripcion}"

@pytest.mark.smoke
def test_login_usuario_valido_smoke(driver):
    """Smoke: al menos un login válido funciona"""
    from pages.login_page import LoginPage
    page = LoginPage(driver)
    page.open()
    page.login("standard_user", "secret_sauce")
    assert page.is_logged_in()
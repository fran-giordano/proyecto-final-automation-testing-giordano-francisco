import pytest
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

class TestLogin:
    """ Caso de prueba: Automatización de Login."""
    
    @pytest.mark.login
    def test_login_exitoso(self, driver, credenciales_validas):
        inventory_page = (
            LoginPage(driver)
            .open()
            .usuario(credenciales_validas["username"])
            .password(credenciales_validas["password"])
            .click()
        )
        assert "/inventory.html" in driver.current_url
        assert "Swag Labs" in driver.title

    @pytest.mark.login
    def test_login_invalido(self, driver, credenciales_invalidas):
        for cred in credenciales_invalidas:
            loginPage = LoginPage(driver).open()
            loginPage.usuario(cred["username"]).password(cred["password"]).click()
            assert loginPage.obtener_error(), f"se esperaba error con {cred}"

    @pytest.mark.login
    def test_usuario_bloqueado(self, driver, usuario_bloqueado):
        login_page = (
            LoginPage(driver)
            .open()
            .usuario(usuario_bloqueado["username"])
            .password(usuario_bloqueado["password"])
            .click()
        )
        assert login_page.obtener_error()

    @pytest.mark.login
    @pytest.mark.parametrize("username, password,deberia_funcionar",[
        ("standard_user", "secret_sauce", True),
        ("invalid_user", "invalid_password", False),
        ("problem_user", "secret_sauce", True),
        ("", "invalid_password", False),
    ])

    
    def test_login_parametrizado(self, driver, username, password, deberia_funcionar):
        login_page = (
            LoginPage(driver)
            .open()
            .usuario(username)
            .password(password)
            .click()
        )
        if deberia_funcionar:
            assert "/inventory.html" in driver.current_url, f"Se esperaba login exitoso con {username}"
        else:
            assert login_page.obtener_error(), f"Se esperaba error con {username}"
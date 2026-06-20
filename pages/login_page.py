from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class LoginPage:
    URL = "https://www.saucedemo.com/"
    _USER_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")  # ← nombre consistente y ID correcto
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(self.driver, 10)

    def open(self):
        self.driver.get(self.URL)
        return self

    def usuario(self, username: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._USER_INPUT))
        campo.clear()
        campo.send_keys(username)
        return self

    def password(self, passw: str):
        campo = self.wait.until(EC.visibility_of_element_located(self._PASSWORD_INPUT))
        campo.clear()
        campo.send_keys(passw)
        return self

    def click(self):
        self.driver.find_element(*self._LOGIN_BUTTON).click()
        return self

    def login(self, username: str, passw: str):
        return self.usuario(username).password(passw).click()

    def obtener_error(self) -> bool:
        try:
            self.wait.until(EC.visibility_of_element_located(self._ERROR_MESSAGE))
            return True
        except:
            return False

    def obtener_error_texto(self) -> str:
        if self.obtener_error():
            return self.driver.find_element(*self._ERROR_MESSAGE).text
        
    def is_logged_in(self) -> bool:
        # Verificar si el usuario ha iniciado sesión exitosamente
        return "inventory" in self.driver.current_url
    
    def has_error(self) -> bool:
        return self.obtener_error()
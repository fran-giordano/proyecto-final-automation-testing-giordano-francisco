import pytest
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options

@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Firefox(service=Service(), options=options)
    driver.implicitly_wait(10)
    yield driver
    driver.quit()

@pytest.fixture
def credenciales_validas():
    return {"username": "standard_user", "password": "secret_sauce"}

@pytest.fixture
def credenciales_invalidas():
    return [
        {"username": "invalid_user", "password": "invalid_password"},
        {"username": "standard_user", "password": "invalid_password"},
        {"username": "", "password": "invalid_password"}
    ]

@pytest.fixture
def usuario_bloqueado():
    return {"username": "locked_out_user", "password": "secret_sauce"}
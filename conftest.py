import pathlib
import pytest
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from webdriver_manager.firefox import GeckoDriverManager
from utils.logger import get_logger

log = get_logger("conftest")

_SCREENSHOTS_DIR = pathlib.Path(__file__).parent / "reports" / "screenshots"
_SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="function")
def driver():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    drv = webdriver.Firefox(service=Service(GeckoDriverManager().install()), options=options)
    drv.implicitly_wait(10)
    log.info("Driver Firefox iniciado")
    yield drv
    log.info("Driver Firefox cerrado")
    drv.quit()


@pytest.fixture
def credenciales_validas():
    return {"username": "standard_user", "password": "secret_sauce"}


@pytest.fixture
def credenciales_invalidas():
    return [
        {"username": "invalid_user", "password": "invalid_password"},
        {"username": "standard_user", "password": "invalid_password"},
        {"username": "", "password": "invalid_password"},
    ]


@pytest.fixture
def usuario_bloqueado():
    return {"username": "locked_out_user", "password": "secret_sauce"}


# ── Hooks ──────────────────────────────────────────────────────────────────────

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when == "call":
        status = "PASÓ" if report.passed else "FALLÓ" if report.failed else "SALTADO"
        log.info(f"[{status}] {item.nodeid}")

    if report.when == "call" and report.failed:
        drv = item.funcargs.get("driver")
        if drv is not None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            nombre = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")
            ruta = _SCREENSHOTS_DIR / f"{timestamp}_{nombre}.png"
            try:
                drv.save_screenshot(str(ruta))
                log.warning(f"Screenshot guardado: {ruta.name}")
                # Adjuntar al reporte pytest-html
                try:
                    from pytest_html import extras
                    if not hasattr(report, "extras"):
                        report.extras = []
                    report.extras.append(extras.image(str(ruta)))
                except Exception:
                    pass
            except Exception as e:
                log.error(f"No se pudo guardar screenshot: {e}")

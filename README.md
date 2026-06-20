# Pre-Entrega: Automatización QA — SauceDemo

Suite de pruebas automatizadas sobre [saucedemo.com](https://www.saucedemo.com) utilizando Selenium WebDriver y Python con patrón Page Object Model (POM).

- **Autor:** Giordano Francisco  
- **Repositorio:** https://github.com/tu-usuario/pre-entrega-Atesting-GiordanoFrancisco

---

## Tecnologías

- Python 3.10+
- Selenium WebDriver
- Pytest + Pytest-HTML

---

## Estructura del Proyecto
```
## Estructura del Proyecto

    pre-entrega-Atesting-GiordanoFrancisco/
    ├── pages/
    │   ├── __init__.py
    │   ├── login_page.py
    │   ├── inventory_page.py
    │   └── cart_page.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_login.py
    │   ├── test_catalog.py
    │   ├── test_cart.py
    │   └── test_e2e.py
    ├── utils/
    │   └── helpers.py
    ├── conftest.py
    ├── pytest.ini
    ├── README.md
    └── requirements.txt
```

---

## Instalación

```bash
pip install -r requirements.txt
```

---

## Ejecución

```bash
# Todos los tests
python -m pytest tests/ -v

# Con reporte HTML
python -m pytest tests/ -v --html=reports/reporte.html

# Por marcador
python -m pytest -m smoke -v
python -m pytest -m regression -v

# Test específico
python -m pytest tests/test_login.py::TestLogin::test_login_exitoso -v
```

---

## Casos de Prueba

| Archivo | Test | Descripción |
|---|---|---|
| `test_login.py` | `test_login_exitoso` | Login con credenciales válidas |
| `test_login.py` | `test_login_invalido` | Login con credenciales inválidas |
| `test_login.py` | `test_usuario_bloqueado` | Usuario bloqueado recibe error |
| `test_login.py` | `test_login_parametrizado` | Múltiples escenarios de login |
| `test_catalog.py` | `test_titulo_inventario` | Verifica título "Products" |
| `test_catalog.py` | `test_productos_visibles` | Verifica presencia de productos |
| `test_catalog.py` | `test_primer_producto_valido` | Nombre y precio válidos |
| `test_cart.py` | `test_agregar_producto_al_carrito` | Agrega y verifica contador |
| `test_cart.py` | `test_eliminar_producto_del_carrito` | Elimina producto del carrito |
| `test_cart.py` | `test_continuar_comprando` | Regresa al inventario |
| `test_e2e.py` | `test_flujo_login_agregar_carrito_logout` | Flujo completo con logout |
| `test_e2e.py` | `test_flujo_agregar_y_eliminar` | Agrega y elimina producto |
| `test_e2e.py` | `test_flujo_multiples_productos` | Múltiples productos en carrito |

---

## Marcadores

| Marcador | Descripción |
|---|---|
| `smoke` | Tests críticos de humo |
| `regression` | Tests de regresión |
| `login` | Funcionalidad de login |
| `catalog` | Funcionalidad de catálogo |
| `cart` | Funcionalidad de carrito |
| `e2e` | Flujos end-to-end |
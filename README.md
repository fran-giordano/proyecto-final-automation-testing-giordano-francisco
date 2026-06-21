# Trabajo Final Integrador — Framework de Automatización QA

Suite completa de pruebas automatizadas sobre [SauceDemo](https://www.saucedemo.com) y la API pública [JSONPlaceholder](https://jsonplaceholder.typicode.com), implementada en Python con Selenium WebDriver, Requests y Pytest siguiendo el patrón Page Object Model (POM).

- **Autor:** Giordano Francisco
- **Repositorio:** https://github.com/fran-giordano/Pre-Entrega-Automation-testing-Giordano-Francisco

---

## Tecnologías

| Herramienta | Versión | Propósito |
|---|---|---|
| Python | 3.10+ | Lenguaje base |
| Selenium WebDriver | 4.20 | Automatización de UI (Firefox) |
| Requests | 2.32 | Pruebas de API REST |
| Pytest | 8.1 | Framework de testing |
| pytest-html | 4.1 | Generación de reportes HTML |
| webdriver-manager | 4.0 | Gestión automática del driver |

---

## Estructura del Proyecto

```
pre-entrega-ATesting-GiordanoFrancisco/
├── pages/
│   ├── login_page.py        # POM — página de login
│   ├── inventory_page.py    # POM — catálogo de productos
│   └── cart_page.py         # POM — carrito de compras
├── tests/
│   ├── test_login.py        # Tests de login (válido, inválido, bloqueado, parametrizado)
│   ├── test_catalog.py      # Tests del catálogo
│   ├── test_cart.py         # Tests del carrito
│   ├── test_e2e.py          # Flujos end-to-end completos
│   ├── test_login_csv.py    # Login parametrizado desde CSV
│   ├── test_cart_json.py    # Carrito parametrizado desde JSON
│   └── test_api.py          # Pruebas de API REST (GET/POST/PUT/DELETE)
├── utils/
│   ├── helpers.py           # Utilidades Selenium (driver, login helper)
│   ├── datos.py             # Lectores de CSV y JSON
│   └── logger.py            # Configuración centralizada de logging
├── datos/
│   ├── login.csv            # Casos de login para parametrización
│   └── productos.json       # Productos para parametrización
├── reports/                 # Generado automáticamente
│   ├── reporte.html         # Reporte HTML de pytest
│   ├── screenshots/         # Capturas en caso de fallo
│   └── tests.log            # Log de ejecución
├── conftest.py              # Fixtures y hooks (driver, screenshots, logging)
├── pytest.ini               # Configuración de pytest y marcadores
└── requirements.txt         # Dependencias del proyecto
```

---

## Instalación

```bash
# 1. Clonar el repositorio
git clone https://github.com/fran-giordano/Pre-Entrega-Automation-testing-Giordano-Francisco.git
cd Pre-Entrega-Automation-testing-Giordano-Francisco

# 2. Crear entorno virtual (recomendado)
python -m venv .venv
.venv\Scripts\activate        # Windows
source .venv/bin/activate     # Linux/Mac

# 3. Instalar dependencias
pip install -r requirements.txt
```

> **Requisito:** Firefox instalado. El driver (geckodriver) se descarga automáticamente.

---

## Ejecución

```bash
# Todos los tests (genera reporte automáticamente en reports/reporte.html)
python -m pytest tests/ -v

# Solo pruebas de UI
python -m pytest tests/ -v -k "not test_api"

# Solo pruebas de API
python -m pytest tests/test_api.py -v

# Por marcador
python -m pytest -m smoke -v
python -m pytest -m regression -v
python -m pytest -m login -v
python -m pytest -m api -v

# Test específico
python -m pytest tests/test_login.py::TestLogin::test_login_exitoso -v
```

El reporte HTML se genera en `reports/reporte.html` y el log en `reports/tests.log`.

---

## Casos de Prueba

### UI — Login (`test_login.py`)

| Test | Tipo | Descripción |
|---|---|---|
| `test_login_exitoso` | Positivo | Login con credenciales estándar válidas |
| `test_login_invalido` | Negativo | Loop sobre credenciales inválidas |
| `test_usuario_bloqueado` | Negativo | Usuario bloqueado recibe mensaje de error |
| `test_login_parametrizado` | Parametrizado | 4 escenarios distintos inline |

### UI — Login desde CSV (`test_login_csv.py`)

| Test | Descripción |
|---|---|
| `test_login_desde_csv` | 7 escenarios leídos de `datos/login.csv` |
| `test_login_usuario_valido_smoke` | Smoke: al menos un login válido funciona |

### UI — Catálogo (`test_catalog.py`)

| Test | Descripción |
|---|---|
| `test_titulo_inventario` | El título de la página es "Products" |
| `test_productos_visibles` | Al menos un producto disponible |
| `test_primer_producto_valido` | Nombre y precio con formato correcto |

### UI — Carrito (`test_cart.py`)

| Test | Descripción |
|---|---|
| `test_agregar_producto_al_carrito` | Agrega y verifica contador y nombre |
| `test_eliminar_producto_del_carrito` | Elimina producto del carrito |
| `test_continuar_comprando` | Botón regresa al inventario |

### UI — Carrito desde JSON (`test_cart_json.py`)

| Test | Descripción |
|---|---|
| `test_agregar_producto_desde_json` | Agrega cada producto del JSON |
| `test_carrito_smoke` | Smoke: funcionalidad básica del carrito |

### UI — E2E (`test_e2e.py`)

| Test | Descripción |
|---|---|
| `test_flujo_login_agregar_carrito_logout` | Login → agregar → carrito → logout |
| `test_flujo_agregar_y_eliminar` | Agregar y eliminar producto |
| `test_flujo_multiples_productos` | Múltiples productos en el carrito |

### API REST — JSONPlaceholder (`test_api.py`)

| Test | Método | Endpoint | Tipo |
|---|---|---|---|
| `test_get_lista_posts` | GET | /posts | Positivo |
| `test_get_post_por_id` | GET | /posts/1 | Positivo |
| `test_get_post_inexistente_retorna_404` | GET | /posts/101 | Negativo |
| `test_get_posts_filtrados_por_usuario` | GET | /posts?userId=1 | Positivo (filtrado) |
| `test_get_comentarios_de_post` | GET | /posts/1/comments | Positivo (anidado) |
| `test_post_crear_post` | POST | /posts | Positivo |
| `test_put_actualizar_post` | PUT | /posts/1 | Positivo |
| `test_delete_post` | DELETE | /posts/1 | Positivo |
| `test_crear_y_verificar_estructura_respuesta` | POST+verificación | /posts | Encadenado |

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
| `api` | Pruebas de API REST |

---

## Interpretación del Reporte

El reporte HTML (`reports/reporte.html`) generado por pytest-html muestra:

- **PASSED** (verde): el test pasó correctamente.
- **FAILED** (rojo): el test falló; se adjunta automáticamente una **captura de pantalla** del estado del navegador en el momento del fallo (solo para tests de UI).
- **ERROR**: error inesperado en el setup o teardown del test.

El archivo `reports/tests.log` registra el detalle paso a paso de cada test con timestamps.

---

## Logging

El módulo `utils/logger.py` provee un logger configurado con dos destinos:

- **Consola** (nivel INFO): muestra el progreso en tiempo real.
- **Archivo** `reports/tests.log` (nivel DEBUG): registro completo con timestamps para auditoría.

Cada test registra: inicio, acciones principales, resultado final (`PASÓ` / `FALLÓ`).

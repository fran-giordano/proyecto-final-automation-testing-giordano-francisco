"""
Pruebas de API REST usando la API pública JSONPlaceholder (https://jsonplaceholder.typicode.com).
Cubre: GET, POST, PUT, DELETE y casos negativos.
Los datos de prueba se definen como fixtures en conftest.py.
"""
import requests
import pytest_check as check
from utils.logger import get_logger

BASE_URL = "https://jsonplaceholder.typicode.com"
log = get_logger("test_api")


class TestAPIPosteos:
    """Pruebas sobre el recurso /posts de JSONPlaceholder."""

    # GET -----------------------------------------------------------------------

    def test_get_lista_posts(self):
        """GET /posts — retorna lista de 100 posts con status 200."""
        log.info("GET /posts — inicio")
        response = requests.get(f"{BASE_URL}/posts")
        log.info(f"Status recibido: {response.status_code}")

        check.equal(response.status_code, 200, "El status debe ser 200")
        body = response.json()
        check.is_true(isinstance(body, list), "La respuesta debe ser una lista")
        check.equal(len(body), 100, "Deben haber 100 posts")
        log.info(f"GET /posts — OK ({len(body)} posts retornados)")

    def test_get_post_por_id(self):
        """GET /posts/1 — recurso existente retorna 200 con estructura correcta."""
        log.info("GET /posts/1 — inicio")
        response = requests.get(f"{BASE_URL}/posts/1")
        log.info(f"Status recibido: {response.status_code}")

        check.equal(response.status_code, 200, "El status debe ser 200")
        post = response.json()
        check.equal(post["id"], 1, "El id debe ser 1")
        check.is_in("userId", post, "Debe existir el campo userId")
        check.is_in("title", post, "Debe existir el campo title")
        check.is_in("body", post, "Debe existir el campo body")
        check.greater(len(post["title"]), 0, "El título no debe estar vacío")
        log.info(f"GET /posts/1 — OK (title: '{post['title'][:40]}...')")

    def test_get_post_inexistente_retorna_404(self):
        """GET /posts/101 — ID fuera de rango debe retornar 404 (caso negativo)."""
        log.info("GET /posts/101 — inicio (caso negativo, solo existen 100 posts)")
        response = requests.get(f"{BASE_URL}/posts/101")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 404, (
            f"Se esperaba 404 para un post inexistente, se recibió {response.status_code}"
        )
        log.info("GET /posts/101 — 404 recibido como se esperaba")

    def test_get_posts_filtrados_por_usuario(self):
        """GET /posts?userId=1 — filtrado por query param retorna solo posts del usuario."""
        log.info("GET /posts?userId=1 — inicio")
        response = requests.get(f"{BASE_URL}/posts", params={"userId": 1})
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        posts = response.json()
        assert len(posts) > 0
        assert all(p["userId"] == 1 for p in posts)
        log.info(f"GET /posts?userId=1 — OK ({len(posts)} posts del usuario 1)")

    def test_get_comentarios_de_post(self):
        """GET /posts/1/comments — recurso anidado retorna lista con estructura correcta."""
        log.info("GET /posts/1/comments — inicio")
        response = requests.get(f"{BASE_URL}/posts/1/comments")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        comentarios = response.json()
        assert isinstance(comentarios, list) and len(comentarios) > 0
        assert "email" in comentarios[0]
        assert "@" in comentarios[0]["email"]
        log.info(f"GET /posts/1/comments — OK ({len(comentarios)} comentarios)")

    # POST ----------------------------------------------------------------------

    def test_post_crear_post(self, post_data):
        """POST /posts — crea un recurso con datos del fixture y verifica la respuesta 201."""
        log.info(f"POST /posts con datos del fixture: {post_data}")
        response = requests.post(f"{BASE_URL}/posts", json=post_data)
        log.info(f"Status recibido: {response.status_code}")

        check.equal(response.status_code, 201, "El status debe ser 201 Created")
        body = response.json()
        check.equal(body["title"], post_data["title"], "El title debe coincidir")
        check.equal(body["body"], post_data["body"], "El body debe coincidir")
        check.equal(body["userId"], post_data["userId"], "El userId debe coincidir")
        check.is_in("id", body, "La respuesta debe incluir el id del recurso creado")
        log.info(f"POST /posts — creado con id={body['id']}")

    # PUT -----------------------------------------------------------------------

    def test_put_actualizar_post(self, post_actualizado):
        """PUT /posts/1 — actualiza recurso con datos del fixture y verifica 200."""
        log.info(f"PUT /posts/1 con datos del fixture: {post_actualizado}")
        response = requests.put(f"{BASE_URL}/posts/1", json=post_actualizado)
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == post_actualizado["id"]
        assert body["title"] == post_actualizado["title"]
        log.info("PUT /posts/1 — actualizado correctamente")

    # DELETE --------------------------------------------------------------------

    def test_delete_post(self):
        """DELETE /posts/1 — elimina recurso y verifica 200."""
        log.info("DELETE /posts/1 — inicio")
        response = requests.delete(f"{BASE_URL}/posts/1")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        log.info("DELETE /posts/1 — eliminado correctamente (200 OK)")

    # Encadenamiento ------------------------------------------------------------

    def test_crear_y_verificar_estructura_respuesta(self, post_data):
        """POST /posts luego verifica que los campos creados coinciden (encadenamiento)."""
        log.info(f"Encadenamiento: POST /posts con fixture: {post_data}")
        r_crear = requests.post(f"{BASE_URL}/posts", json=post_data)
        assert r_crear.status_code == 201
        post_creado = r_crear.json()
        log.info(f"POST exitoso — id={post_creado['id']}, verificando campos")

        check.equal(post_creado["title"], post_data["title"])
        check.equal(post_creado["body"], post_data["body"])
        check.equal(post_creado["userId"], post_data["userId"])
        check.is_true(isinstance(post_creado["id"], int), "El id debe ser un entero")
        log.info("Encadenamiento POST -> verificacion — OK")

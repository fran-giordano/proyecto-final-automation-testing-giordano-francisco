"""
Pruebas de API REST usando la API pública JSONPlaceholder (https://jsonplaceholder.typicode.com).
Cubre: GET, POST, PUT, DELETE, filtrado, recursos anidados y casos negativos.
"""
import requests
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
        assert response.status_code == 200
        body = response.json()
        assert isinstance(body, list)
        assert len(body) == 100, f"Se esperaban 100 posts, se recibieron {len(body)}"
        log.info(f"GET /posts — OK ({len(body)} posts retornados)")

    def test_get_post_por_id(self):
        """GET /posts/1 — recurso existente retorna 200 con estructura correcta."""
        log.info("GET /posts/1 — inicio")
        response = requests.get(f"{BASE_URL}/posts/1")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        post = response.json()
        assert post["id"] == 1
        assert "userId" in post
        assert "title" in post
        assert "body" in post
        assert len(post["title"]) > 0, "El título no debe estar vacío"
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
        assert len(posts) > 0, "El filtro debe retornar al menos un post"
        assert all(p["userId"] == 1 for p in posts), "Todos los posts deben pertenecer al userId=1"
        log.info(f"GET /posts?userId=1 — OK ({len(posts)} posts del usuario 1)")

    def test_get_comentarios_de_post(self):
        """GET /posts/1/comments — recurso anidado retorna lista con estructura correcta."""
        log.info("GET /posts/1/comments — inicio")
        response = requests.get(f"{BASE_URL}/posts/1/comments")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        comentarios = response.json()
        assert isinstance(comentarios, list)
        assert len(comentarios) > 0
        primer_comentario = comentarios[0]
        assert "postId" in primer_comentario
        assert "email" in primer_comentario
        assert "@" in primer_comentario["email"]
        log.info(f"GET /posts/1/comments — OK ({len(comentarios)} comentarios)")

    # POST ----------------------------------------------------------------------

    def test_post_crear_post(self):
        """POST /posts — crea un recurso y verifica la respuesta 201."""
        payload = {"title": "TFI QA Automation", "body": "Framework de testing con Pytest y Requests", "userId": 1}
        log.info(f"POST /posts con payload: {payload}")
        response = requests.post(f"{BASE_URL}/posts", json=payload)
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 201
        body = response.json()
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        assert body["userId"] == payload["userId"]
        assert "id" in body, "La respuesta debe incluir el id del recurso creado"
        log.info(f"POST /posts — creado con id={body['id']}")

    # PUT -----------------------------------------------------------------------

    def test_put_actualizar_post(self):
        """PUT /posts/1 — actualiza recurso existente y verifica 200."""
        payload = {"id": 1, "title": "Título actualizado", "body": "Contenido actualizado", "userId": 1}
        log.info(f"PUT /posts/1 con payload: {payload}")
        response = requests.put(f"{BASE_URL}/posts/1", json=payload)
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        body = response.json()
        assert body["id"] == 1
        assert body["title"] == payload["title"]
        assert body["body"] == payload["body"]
        log.info(f"PUT /posts/1 — actualizado correctamente")

    # DELETE --------------------------------------------------------------------

    def test_delete_post(self):
        """DELETE /posts/1 — elimina recurso y verifica 200."""
        log.info("DELETE /posts/1 — inicio")
        response = requests.delete(f"{BASE_URL}/posts/1")
        log.info(f"Status recibido: {response.status_code}")
        assert response.status_code == 200
        log.info("DELETE /posts/1 — eliminado correctamente (200 OK)")

    # Encadenamiento ------------------------------------------------------------

    def test_crear_y_verificar_estructura_respuesta(self):
        """POST /posts luego verifica que los campos creados coinciden (encadenamiento)."""
        payload = {"title": "Test Encadenado", "body": "Verificacion de estructura", "userId": 5}
        log.info("Encadenamiento: POST /posts")
        r_crear = requests.post(f"{BASE_URL}/posts", json=payload)
        assert r_crear.status_code == 201
        post_creado = r_crear.json()
        log.info(f"POST exitoso — id={post_creado['id']}, verificando campos")

        assert post_creado["title"] == payload["title"]
        assert post_creado["body"] == payload["body"]
        assert post_creado["userId"] == payload["userId"]
        assert isinstance(post_creado["id"], int)

        log.info("Encadenamiento POST -> verificacion de estructura — OK")

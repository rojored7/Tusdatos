from fastapi.testclient import TestClient
from main import app 
import pytest

client = TestClient(app)

@pytest.fixture
def access_token():
    response = client.post("/token", data={"username": "Cristian", "password": "secret1234"})
    assert response.status_code == 200
    return response.json()["access_token"]

def test_authentication():
    
    response = client.post("/token", data={"username": "Felipe", "password": "malaClave"})
    assert response.status_code == 401
    assert response.json() == {"detail": "Incorrect username or password"}

    response = client.post("/token", data={"username": "Cristian", "password": "secret1234"})
    assert response.status_code == 200
    assert "access_token" in response.json()
    access_token = response.json()["access_token"]

    return access_token

def test_read_json_authenticated(access_token):
    # Intento de acceso sin token
    response = client.get("/procesos/")
    assert response.status_code == 401, "Se esperaba un 401 Unauthorized por falta de token"

    # Acceso con token
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/procesos/", headers=headers)
    assert response.status_code == 200, "Se esperaba un 200 OK al acceder con un token válido"
   
def test_read_json_file_not_found(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    response = client.get("/procesos/", headers=headers)
    # Ajusta el código de estado esperado y el mensaje según la implementación de tu endpoint
    assert response.status_code == 404, "Se esperaba un 404 Not Found cuando el archivo JSON no se encuentra"
    assert response.json() == {"error": "Archivo JSON no encontrado."}
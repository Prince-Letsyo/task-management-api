import pytest
from app.main import app
from app.db import AsyncSessionLocal
from fastapi.testclient import TestClient


@pytest.fixture
def client(session, mock_user):

    app.dependency_overrides[AsyncSessionLocal] = session

    with TestClient(app) as c:
        sign_up_user = mock_user
        user_data = {
            "username": sign_up_user["username"],
            "email": sign_up_user["email"],
            "password": sign_up_user["password"],
        }
        response = c.post("/auth/sign_up", json=user_data)
        data = response.json()
        c.headers["Authorization"] = (
            f"{data["token"]["token_type"]} {data["token"]["access_token"]}"
        )
        yield c


@pytest.fixture
def created_task(client):
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "status": "pending",
    }
    response = client.post("/tasks/", json=task_data)
    return response.json()


@pytest.mark.usefixtures("client")
class TestTaskRoutes:
    def test_create_task(self, client):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "status": "pending",
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["status"] == task_data["status"]
        assert "id" in data

    def test_get_tasks(self, client, mock_user, created_task):
        sign_up_user = mock_user
        user_data = {
            "username": sign_up_user["username"],
            "email": sign_up_user["email"],
            "password": sign_up_user["password"],
        }
        response = client.post("/auth/sign_up", json=user_data)
        data = response.json()
        response = client.get("/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least one task should exist from previous test
        assert "title" in data[0]
        assert "description" in data[0] or data[0]["description"] is None
        assert "status" in data[0]
        assert "id" in data[0]

    def test_get_task(self, client, created_task):
        task_id = created_task["id"]
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert "title" in data
        assert "description" in data or data["description"] is None
        assert "status" in data

    def test_update_task(self, client, created_task):
        task_id = created_task["id"]
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "status": "completed",
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["status"] == update_data["status"]

    def test_delete_task(self, client, created_task):
        task_id = created_task["id"]
        response = client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        # Verify the task is deleted
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 404

    def test_get_nonexistent_task(self, client):
        response = client.get("/tasks/9999")  # Assuming 9999 does not exist
        assert response.status_code == 404

    def test_update_nonexistent_task(self, client):
        update_data = {
            "title": "Nonexistent Task",
            "description": "This task does not exist",
            "status": "completed",
        }
        response = client.put(
            "/tasks/9999", json=update_data
        )  # Assuming 9999 does not exist
        assert response.status_code == 404

    def test_delete_nonexistent_task(self, client):
        response = client.delete("/tasks/9999")  # Assuming 9999 does not exist
        assert response.status_code == 404
        assert response.json() == {"detail": "Task with id 9999 not found"}

    def test_partial_update_task(self, client, created_task):
        task_id = created_task["id"]
        partial_update_data = {
            "description": "Partially updated description",
        }
        response = client.patch(f"/tasks/{task_id}", json=partial_update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["description"] == partial_update_data["description"]
        assert data["title"] == created_task["title"]
        assert data["status"] == created_task["status"]

    def test_partial_update_nonexistent_task(self, client):
        partial_update_data = {
            "description": "Trying to update a nonexistent task",
        }
        response = client.patch(
            "/tasks/9999", json=partial_update_data
        )  # Assuming 9999 does not exist
        assert response.status_code == 404
        assert response.json() == {"detail": "Task with id 9999 not found"}

    def test_create_task_missing_title(self, client):
        task_data = {
            "description": "This task has no title",
            "status": "in-progress",
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422  # Unprocessable Entity
        data = response.json()
        assert data["detail"][0]["loc"] == ["body", "title"]

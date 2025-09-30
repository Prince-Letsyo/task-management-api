import pytest
from app import app
from fastapi.testclient import TestClient


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def created_task(client):
    task_data = {
        "title": "Test Task",
        "description": "This is a test task",
        "due_date": "2024-12-31",
    }
    response = client.post("/tasks/", json=task_data)
    assert response.status_code == 201
    return response.json()


class TestTaskRoutes:
    def setup_method(self):
        self.task_id = None

    def test_create_task(self, client):
        task_data = {
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2024-12-31",
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["due_date"] == task_data["due_date"]

    def test_get_tasks(self, client, created_task):
        response = client.get("/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) >= 1  # At least one task should exist from previous test
        assert "title" in data[0]
        assert "description" in data[0] or data[0]["description"] is None
        assert (
            "due_date" in data[0]
            or data[0]["due_date"] is None
            or data[0]["due_date"] is not None
        )  # due_date can be null or a valid date string
        assert "id" in data[0]

    def test_get_task(self, client, created_task):
        task_id = created_task["id"]
        print(f"Testing get_task with task_id: {task_id}")
        response = client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert "title" in data
        assert "description" in data or data["description"] is None
        assert (
            "due_date" in data
            or data["due_date"] is None
            or data["due_date"] is not None
        )  # due_date can be null or a valid date string

    def test_update_task(self, client, created_task):
        task_id = created_task["id"]
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "due_date": "2024-11-30",
        }
        response = client.put(f"/tasks/{task_id}", json=update_data)
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == update_data["title"]
        assert data["description"] == update_data["description"]
        assert data["due_date"] == update_data["due_date"]

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
            "due_date": "2024-10-10",
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
        # Ensure other fields remain unchanged
        print(f"Created task for partial update test: {created_task}")
        print(f"Response data after partial update: {data}")
        assert data["title"] == created_task["title"]
        assert data["due_date"] == created_task["due_date"]

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
            "due_date": "2024-12-31",
        }
        response = client.post("/tasks/", json=task_data)
        assert response.status_code == 422  # Unprocessable Entity
        data = response.json()
        assert data["detail"][0]["loc"] == ["body", "title"]

    
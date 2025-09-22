from fastapi.testclient import TestClient
from src import app


class TestTaskSchemas:
    def test_task_schema(self):
        task_data = {
            "id": 1,
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2024-12-31",
        }
        response = TestClient(app).post("/tasks/", json=task_data)
        assert response.status_code == 201
        data = response.json()
        assert data["id"] == task_data["id"]
        assert data["title"] == task_data["title"]
        assert data["description"] == task_data["description"]
        assert data["due_date"] == task_data["due_date"]

    def test_task_create_schema(self):
        task_create_data = {
            "title": "New Task",
            "description": "This is a new task",
            "due_date": "2024-11-30",
        }
        response = TestClient(app).post("/tasks/", json=task_create_data)
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == task_create_data["title"]
        assert data["description"] == task_create_data["description"]
        assert data["due_date"] == task_create_data["due_date"]

    def test_task_update_schema(self):
        # First, create a task to update
        create_response = TestClient(app).post(
            "/tasks/",
            json={
                "title": "Task to Update",
                "description": "This task will be updated",
                "due_date": "2024-10-31",
            },
        )
        assert create_response.status_code == 201
        created_task = create_response.json()

        # Now, update the created task
        update_data = {
            "title": "Updated Task Title",
            "description": "Updated description",
            "due_date": "2024-12-31",
        }
        update_response = TestClient(app).put(
            f"/tasks/{created_task['id']}", json=update_data
        )
        assert update_response.status_code == 200
        updated_task = update_response.json()
        assert updated_task["title"] == update_data["title"]
        assert updated_task["description"] == update_data["description"]
        assert updated_task["due_date"] == update_data["due_date"]

    def test_task_error_schema(self):
        response = TestClient(app).get(
            "/tasks/9999"
        )  # Assuming task with id 9999 does not exist
        assert response.status_code == 404
        data = response.json()
        assert "error" in data["detail"]
        assert data["detail"]["error"] == "Task with id 9999 not found"

    def test_task_create_schema_missing_title(self):
        task_create_data = {
            "description": "This is a new task without a title",
            "due_date": "2024-11-30",
        }
        response = TestClient(app).post("/tasks/", json=task_create_data)
        assert response.status_code == 422  # Unprocessable Entity
        data = response.json()
        assert data["detail"][0]["loc"] == ["body", "title"]
        assert data["detail"][0]["msg"] == "Field required"

    # def test_task_create_schema_invalid_due_date(self):
    #     task_create_data = {
    #         "title": "New Task with Invalid Date",
    #         "description": "This is a new task",
    #         "due_date": "30-11-2024",  # Invalid date format
    #     }
    #     response = TestClient(app).post("/tasks/", json=task_create_data)
    #     assert response.status_code == 400  # Bad Request
    #     data = response.json()
    #     assert "error" in data["detail"]
    #     assert data["detail"]["error"] == "Task with invalid date format"

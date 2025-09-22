from fastapi.testclient import TestClient
from src import app

client = TestClient(app)

class TestTaskRoutes:
    @classmethod
    def setup_class(cls):
        # Setup code before any tests run (e.g., clear tasks if needed)
        cls.client = client
        # Optionally clear all tasks before running tests
        cls._clear_all_tasks()

    @classmethod
    def teardown_class(cls):
        # Teardown code after all tests run (e.g., cleanup tasks if needed)
        cls._clear_all_tasks()

    def setup_method(self, method):
        # Setup before each test method
        self._clear_all_tasks()

    def teardown_method(self, method):
        # Teardown after each test method
        self._clear_all_tasks()

    @classmethod
    def _clear_all_tasks(cls):
        response = cls.client.get("/tasks/")
        if response.status_code == 200:
            for task in response.json():
                cls.client.delete(f"/tasks/{task['id']}")

    def create_task(
        self,
        title="Test Task",
        description="This is a test task",
        due_date="2024-12-31",
    ):
        response = self.client.post(
            "/tasks/",
            json={
                "title": title,
                "description": description,
                "due_date": due_date,
            },
        )
        assert response.status_code == 201
        return response.json()

    def test_create_task(self):
        data = self.create_task()
        assert data["title"] == "Test Task"
        assert data["description"] == "This is a test task"
        assert data["due_date"] == "2024-12-31"

    def test_get_tasks(self):
        self.create_task()
        response = self.client.get("/tasks/")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    def test_get_task(self):
        task = self.create_task(
            title="Test Task for Get", description="This is a test task for get"
        )
        task_id = task["id"]
        response = self.client.get(f"/tasks/{task_id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Test Task for Get"
        assert data["description"] == "This is a test task for get"
        assert data["due_date"] == "2024-12-31"

    def test_update_task(self):
        task = self.create_task(
            title="Test Task for Update", description="This is a test task for update"
        )
        task_id = task["id"]
        response = self.client.put(
            f"/tasks/{task_id}",
            json={
                "title": "Updated Test Task",
                "description": "This task has been updated",
                "due_date": "2025-01-31",
            },
        )
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == task_id
        assert data["title"] == "Updated Test Task"
        assert data["description"] == "This task has been updated"
        assert data["due_date"] == "2025-01-31"

    def test_delete_task(self):
        task = self.create_task(
            title="Test Task for Delete", description="This is a test task for delete"
        )
        task_id = task["id"]
        response = self.client.delete(f"/tasks/{task_id}")
        assert response.status_code == 204
        get_response = self.client.get(f"/tasks/{task_id}")
        assert get_response.status_code == 404

    def test_get_nonexistent_task(self):
        response = self.client.get("/tasks/9999")
        assert response.status_code == 404

    def test_update_nonexistent_task(self):
        response = self.client.put(
            "/tasks/9999",
            json={
                "title": "Non-existent Task",
                "description": "Trying to update a non-existent task",
                "due_date": "2025-01-31",
            },
        )
        assert response.status_code == 404
    
    def test_delete_nonexistent_task(self):
        response = self.client.delete("/tasks/9999")
        assert response.status_code == 404
    
    # def test_create_task_invalid_date(self):
    #     response = self.client.post(
    #         "/tasks/",
    #         json={
    #             "title": "Task with Invalid Date",
    #             "description": "This task has an invalid date",
    #             "due_date": "31-12-2024",  # Invalid format
    #         },
    #     )
    #     assert response.status_code == 422
    #     data = response.json()
    #     assert "error" in data.details
    #     assert data["error"] == "Task with invalid date format"
        
    # def test_update_task_invalid_date(self):
    #     task = self.create_task(
    #         title="Test Task for Update Invalid Date", 
    #         description="This is a test task for update with invalid date"
    #     )
    #     task_id = task["id"]
    #     response = self.client.put(
    #         f"/tasks/{task_id}",
    #         json={
    #             "title": "Updated Test Task with Invalid Date",
    #             "description": "This task has been updated with invalid date",
    #             "due_date": "31-01-2025",  # Invalid format
    #         },
    #     )
    #     assert response.status_code == 400
    #     data = response.json()
    #     assert "error" in data
    #     assert data["error"] == "Task with invalid date format"
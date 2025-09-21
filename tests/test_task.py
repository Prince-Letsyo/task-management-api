from fastapi.testclient import TestClient
from src import app

client = TestClient(app)


def test_create_task():
    response = client.post(
        "api/tasks/",
        json={
            "title": "Test Task",
            "description": "This is a test task",
            "due_date": "2024-12-31T23:59:59",
        },
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "This is a test task"
    assert data["due_date"] == "2024-12-31T23:59:59"


def test_get_tasks():
    response = client.get("api/tasks/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_get_task():
    # First, create a task to ensure there is one to retrieve
    create_response = client.post(
        "api/tasks/",
        json={
            "title": "Test Task for Get",
            "description": "This is a test task for get",
            "due_date": "2024-12-31T23:59:59",
        },
    )
    task_id = create_response.json()["id"]

    response = client.get(f"api/tasks/{task_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Test Task for Get"
    assert data["description"] == "This is a test task for get"
    assert data["due_date"] == "2024-12-31T23:59:59"


def test_update_task():
    # First, create a task to ensure there is one to update
    create_response = client.post(
        "api/tasks/",
        json={
            "title": "Test Task for Update",
            "description": "This is a test task for update",
            "due_date": "2024-12-31T23:59:59",
        },
    )
    task_id = create_response.json()["id"]

    response = client.put(
        f"api/tasks/{task_id}",
        json={
            "title": "Updated Test Task",
            "description": "This task has been updated",
            "due_date": "2025-01-31T23:59:59",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == task_id
    assert data["title"] == "Updated Test Task"
    assert data["description"] == "This task has been updated"
    assert data["due_date"] == "2025-01-31T23:59:59"

def test_delete_task():
    # First, create a task to ensure there is one to delete
    create_response = client.post(
        "api/tasks/",
        json={
            "title": "Test Task for Delete",
            "description": "This is a test task for delete",
            "due_date": "2024-12-31T23:59:59",
        },
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"api/tasks/{task_id}")
    assert response.status_code == 204

    # Verify the task has been deleted
    get_response = client.get(f"api/tasks/{task_id}")
    assert get_response.status_code == 404
    
def test_get_nonexistent_task():
    response = client.get("api/tasks/9999")  # Assuming 9999 is a non-existent ID
    assert response.status_code == 404
    
    
def test_update_nonexistent_task(): 
    response = client.put(
        "api/tasks/9999",  # Assuming 9999 is a non-existent ID
        json={
            "title": "Non-existent Task",
            "description": "Trying to update a non-existent task",
            "due_date": "2025-01-31T23:59:59",
        },
    )
    assert response.status_code == 404
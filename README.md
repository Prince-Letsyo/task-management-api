# Task Management API

A simple RESTful API for managing tasks, built with FastAPI and Pydantic. This project demonstrates basic CRUD operations with in-memory storage, making it ideal for learning, prototyping, or as a foundation for more complex systems.

## Features

- Retrieve all tasks
- Get a task by ID
- Create new tasks
- Update or partially update tasks
- Delete tasks
- In-memory data storage (no database required)

## Project Structure

```
src/
  main.py                # FastAPI app entry point
  api/
    endpoints/
      task.py            # Task-related API endpoints
  models/
    task.py              # Task data model and in-memory storage
  schemas/
    task.py              # Pydantic schemas for validation
  services/
    task_services.py     # Business logic for tasks
```

## Installation

1. **Clone the repository:**
   ```sh
   git clone https://github.com/yourusername/task-management-api.git
   cd task-management-api
   ```

2. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```
   Or, if using [pyproject.toml](pyproject.toml):
   ```sh
   pip install .
   ```

3. **Run the API server:**
   ```sh
   uvicorn src.main:app --reload
   ```

## Usage

Once the server is running, access the interactive API docs at [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs).

## API Endpoints

### Get All Tasks

- **GET** `/api/tasks`
- **Response:** List of tasks

### Get Task by ID

- **GET** `/api/tasks/{task_id}`
- **Response:** Task object or error message

### Create Task

- **POST** `/api/tasks`
- **Body:**
  ```json
  {
    "title": "Task Title",
    "description": "Optional description",
    "due_date": "YYYY-MM-DD"
  }
  ```
- **Response:** Created task object

### Update Task

- **PUT** `/api/tasks/{task_id}`
- **Body:**
  ```json
  {
    "title": "Updated Title",
    "description": "Updated description",
    "due_date": "YYYY-MM-DD"
  }
  ```
- **Response:** Updated task object

### Partial Update Task

- **PATCH** `/api/tasks/{task_id}`
- **Body:** (Any subset of fields)
  ```json
  {
    "title": "New Title"
  }
  ```
- **Response:** Updated task object

### Delete Task

- **DELETE** `/api/tasks/{task_id}`
- **Response:** Success message or error

## Example Request

```sh
curl -X POST "http://127.0.0.1:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Write docs", "description": "Complete the README", "due_date": "2025-09-30"}'
```

## Development

- Python 3.13+
- FastAPI
- Uvicorn

## Further Reading

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [Uvicorn Documentation](https://www.uvicorn.org/)

## License

MIT

## Author

Prince
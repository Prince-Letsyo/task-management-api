# Task Management API

A simple FastAPI-based RESTful API for managing tasks. This project demonstrates basic CRUD operations using Python 3.13, FastAPI, and Pydantic.

## Features

- Retrieve all tasks
- Get a task by ID
- Create new tasks
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
    "description": "Optional description"
  }
  ```
- **Response:** Created task object

## Example Request

```sh
curl -X POST "http://127.0.0.1:8000/api/tasks" \
     -H "Content-Type: application/json" \
     -d '{"title": "Write docs", "description": "Complete the README"}'
```

## Development

- Python 3.13+
- FastAPI
- Uvicorn

## License

MIT

## Author

Prince

# Task Management API

A RESTful API built with **FastAPI** + **SQLModel** for managing tasks.  
This project is intended as a starter or demo project; you can extend it with user authentication, multi‑tenant features, etc.

---

## Table of Contents

- [Task Management API](#task-management-api)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Tech Stack](#tech-stack)
  - [Directory Structure](#directory-structure)
  - [Getting Started](#getting-started)
    - [Prerequisites](#prerequisites)
    - [Installation](#installation)
    - [Configuration](#configuration)
    - [Running the Server](#running-the-server)
  - [API Reference](#api-reference)
    - [Base URL](#base-url)
    - [Endpoints](#endpoints)
      - [Example: Create Task](#example-create-task)
      - [Example: Update Task](#example-update-task)
      - [Example: Delete Task](#example-delete-task)
  - [Data Models](#data-models)
    - [Task](#task)
  - [Testing](#testing)
  - [Production / Deployment Notes](#production--deployment-notes)
  - [Roadmap / Future Enhancements](#roadmap--future-enhancements)
  - [License](#license)

---

## Features

- CRUD (Create, Read, Update, Delete) operations for tasks  
- Input and output validation via Pydantic / SQLModel  
- Auto-generated API documentation (Swagger / ReDoc)  
- Lightweight — uses SQLite by default (suitable for development)  
- Clean layered architecture for maintainability  

---

## Tech Stack

- Python ≥ 3.13  
- FastAPI  
- SQLModel (combines Pydantic + SQLAlchemy)  
- SQLite (default DB)  
- Uvicorn (ASGI server)  
- Pytest (for testing)  

---

## Directory Structure

Here is your project’s layout:

```
task-management-api/
├── app/
│   ├── api/               # Routers / endpoint definitions  
│   ├── core/              # Configuration, DB setup  
│   ├── models/            # SQLModel models  
│   ├── repositories/      # Data-access layer  
│   ├── schemas/            # Pydantic / SQLModel request & response schemas  
│   ├── services/          # Business logic / use-cases  
│   ├── main.py             # FastAPI app entrypoint  
│   └── __init__.py
├── tests/                  # Test suite  
├── .env_dev                 # Sample / template environment file  
├── database.db              # The SQLite database file (for dev)  
├── test.db                  # Possibly test DB file  
├── pyproject.toml / requirements.txt  # Dependency declarations  
├── .gitignore  
└── README.md  
```

**Notes / Observations:**

- The top‑level directory is `app/`, not `src/`.  
- All your application logic (routers, models, services etc.) lives inside `app/`.  
- You have a `database.db` file for dev, and a separate `test.db`.  
- `.env_dev` is your sample environment variables file.  

When writing documentation or instructions, refer to `app.main:app` rather than `src.main:app` when launching the server.

---

## Getting Started

### Prerequisites

- Python 3.13 or above  
- Virtual environment tool (venv, pipenv, poetry, etc.)

### Installation

```bash
git clone https://github.com/Prince-Letsyo/task-management-api.git
cd task-management-api

# Create & activate venv
python -m venv venv
source venv/bin/activate        # macOS / Linux
# On Windows: venv\Scriptsctivate

# Install dependencies
pip install -r requirements.txt
```

(If you use Poetry / pyproject.toml, you may use `poetry install` instead.)

### Configuration

1. Copy `.env_dev` to `.env`  
2. Open `.env` and edit the following (or add more as needed):

```text
DATABASE_URL=sqlite:///./database.db
SECRET_KEY=your-very-strong-secret
```

3. If you want to use another database (PostgreSQL, MySQL, etc.), change `DATABASE_URL` accordingly.

### Running the Server

From project root:

```bash
uvicorn app.main:app --reload
```

Once running:

- Swagger UI: `http://localhost:8000/docs`  
- ReDoc: `http://localhost:8000/redoc`  

---

## API Reference

### Base URL

```
http://localhost:8000/api/v1
```

### Endpoints

| Method  | Path                | Description                  | Request Body / Query Params            | Response / Notes                     |
|--------|---------------------|-------------------------------|----------------------------------------|--------------------------------------|
| GET    | `/tasks/`            | List all tasks                | —                                      | 200 OK → list of task objects        |
| POST   | `/tasks/`            | Create a new task             | JSON: title, description, status       | 201 Created → created task object    |
| GET    | `/tasks/{task_id}`   | Retrieve task by ID           | Path param: `task_id`                  | 200 OK → task object or 404          |
| PUT    | `/tasks/{task_id}`   | Update a task                 | JSON: title, description, status       | 200 OK → updated task object         |
| DELETE | `/tasks/{task_id}`   | Delete a task                 | Path param: `task_id`                  | 204 No Content on success            |

#### Example: Create Task

**Request**

```
POST /tasks/
Content-Type: application/json

{
  "title": "Write documentation",
  "description": "Draft and polish README",
  "status": "pending"
}
```

**Response (201 Created)**

```json
{
  "id": 1,
  "title": "Write documentation",
  "description": "Draft and polish README",
  "status": "pending"
}
```

#### Example: Update Task

```
PUT /tasks/1
Content-Type: application/json

{
  "title": "Write docs",
  "description": "Include full API reference",
  "status": "in-progress"
}
```

Response:

```json
{
  "id": 1,
  "title": "Write docs",
  "description": "Include full API reference",
  "status": "in-progress"
}
```

#### Example: Delete Task

```
DELETE /tasks/1
```

Response: `204 No Content`

---

## Data Models

### Task

| Field        | Type       | Required | Description                          |
|--------------|------------|----------|--------------------------------------|
| `id`         | `int`      | Yes      | Auto-generated unique identifier     |
| `title`      | `str`      | Yes      | Task title                           |
| `description`| `str` / `None` | No    | Extra detail or notes                |
| `status`     | `str` enum | Yes      | One of: `pending`, `in-progress`, `completed` |

These models are defined in your `app/models/` and `app/schemas/` directories, using SQLModel (Pydantic + SQLAlchemy).  

---

## Testing

To run your tests:

```bash
pytest
```

You presumably have tests within `tests/` that cover creation, fetching, updating, deleting, and error cases (e.g. 404).  

If you want, you can integrate tests into CI (GitHub Actions, etc.).

---

## Production / Deployment Notes

- Replace SQLite with a production-grade DB (PostgreSQL, MySQL, etc.)  
- Introduce **database migrations**, for example via **Alembic**  
- Add **authentication / authorization** (JWT, OAuth2, etc.)  
- Add **pagination**, **filtering**, **sorting** in list endpoints  
- Add proper **logging**, **error handling**, **rate limiting**, **monitoring / metrics**  
- Containerize with **Docker** or **docker-compose**  
- Use an ASGI server configuration (e.g. Uvicorn + Gunicorn)  
- Use environment-based config (dev, staging, prod)  
- Secure and manage secrets (avoid committing `.env` with real secrets)  
- Consider caching, background tasks, webhooks, etc., as your app grows  

---

## Roadmap / Future Enhancements

- ✅ Basic task CRUD (already implemented)  
- ✅ User registration, login, multi-user support  
- Tasks grouping (projects, tags, categories)  
- Due dates, reminders, notifications  
- Subtasks or task hierarchies  
- Soft-delete / archiving  
- Audit trails / history logs  
- Webhooks / external integrations  
- Search, full-text query support  

---

## License

This project is licensed under the **MIT License**.

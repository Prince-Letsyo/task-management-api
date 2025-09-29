# 📌 Task Management API

A simple **FastAPI-powered RESTful API** for managing tasks.  
Currently, tasks are stored in a local **SQLite** database, making this ideal for demos, learning, or as a starter template for production APIs.

---

## 🚀 Tech Stack

- **Python** ≥ 3.13  
- **FastAPI** — API framework  
- **Pydantic** — request/response validation  
- **SQLModel** — ORM + database interaction  
- **SQLite** — default database (swap out for Postgres/MySQL in prod)  
- **Uvicorn** — ASGI server  
- **Pytest** — testing framework  

---

## 📂 Project Structure

```
task-management-api/
├── src/
│   ├── core/              # Core configurations (DB, settings)
│   ├── models/            # SQLModel models
│   ├── repositories/      # Database access layer
│   ├── services/          # Business logic
│   ├── api/               # FastAPI routers & endpoints
│   ├── schemas/           # Pydantic request/response schemas
│   ├── main.py            # Application entry point
│   └── __init__.py
├── tests/                 # Test suite
├── .env.dev               # Dev environment variables
├── requirements.txt        # Dependencies
├── pyproject.toml          # Poetry project file (if used)
└── README.md
```

---

## ⚙️ Getting Started

### Prerequisites
- Python **3.13+**
- Virtual environment (`venv`, `poetry`, or `pipenv`)

### Installation

```bash
git clone https://github.com/Prince-Letsyo/task-management-api.git
cd task-management-api

# Create & activate virtual environment
python -m venv venv
source venv/bin/activate   # Linux/Mac
venv\Scriptsctivate      # Windows

# Install dependencies
pip install -r requirements.txt
```

### Configuration

Copy `.env.dev` to `.env` and set required variables:

```ini
DATABASE_URL=sqlite:///./tasks.db
SECRET_KEY=super-secret-key
```

### Running the Server

```bash
uvicorn src.main:app --reload
```

The API will be available at:  
👉 [http://localhost:8000/docs](http://localhost:8000/docs) (Swagger UI)  
👉 [http://localhost:8000/redoc](http://localhost:8000/redoc) (ReDoc UI)  

---

## 🔑 Authentication

Currently, no authentication is enforced.  
*(You can extend with JWT / OAuth2 if required.)*

---

## 📖 API Reference

### Base URL
```
http://localhost:8000/api/v1
```

### Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/tasks/` | List all tasks |
| POST   | `/tasks/` | Create a new task |
| GET    | `/tasks/{task_id}` | Retrieve a task |
| PUT    | `/tasks/{task_id}` | Update a task |
| DELETE | `/tasks/{task_id}` | Delete a task |

---

### Create Task

**Request**  
`POST /tasks/`

```json
{
  "title": "Finish API docs",
  "description": "Write documentation for the project",
  "status": "pending"
}
```

**Response (201 Created)**

```json
{
  "id": 1,
  "title": "Finish API docs",
  "description": "Write documentation for the project",
  "status": "pending",
}
```

---

### List Tasks

**Request**  
`GET /tasks/`

**Response (200 OK)**

```json
[
  {
    "id": 1,
    "title": "Finish API docs",
    "description": "Write documentation for the project",
    "status": "pending"
  }
]
```

---

### Retrieve Task

**Request**  
`GET /tasks/1`

**Response (200 OK)**

```json
{
  "id": 1,
  "title": "Finish API docs",
  "description": "Write documentation for the project",
  "status": "pending"
}
```

---

### Update Task

**Request**  
`PUT /tasks/1`

```json
{
  "title": "Finish API docs",
  "description": "Complete with Markdown + PDF export",
  "status": "in-progress"
}
```

**Response (200 OK)**

```json
{
  "id": 1,
  "title": "Finish API docs",
  "description": "Complete with Markdown + PDF export",
  "status": "in-progress",
}
```

---

### Delete Task

**Request**  
`DELETE /tasks/1`

**Response (204 No Content)**

---

## 🗂️ Data Models

### Task

| Field       | Type     | Required | Description |
|-------------|----------|----------|-------------|
| id          | int      | Yes      | Unique ID |
| title       | string   | Yes      | Task title |
| description | string   | No       | Task details |
| status      | enum     | Yes      | `pending`, `in-progress`, `completed` |


---

## 🧪 Testing

Run the tests with:

```bash
pytest
```

---

## 🚀 Deployment

- Replace SQLite with Postgres/MySQL for production
- Run database migrations (Alembic recommended)
- Use `.env` for environment configs
- Deploy with Docker, Gunicorn + Uvicorn, or on platforms like Render/Heroku

---

## 📌 Roadmap

- ✅ CRUD operations for tasks  
- 🔲 User authentication & authorization  
- 🔲 Task categorization & tags  
- 🔲 Project-level grouping  

---

## 📄 License

This project is licensed under the **MIT License**.

# Task Management API

A simple **FastAPI**-powered RESTful API for managing tasks.  
Currently, tasks are stored in a local **SQLite** database, making this ideal for demos, learning, or as a starter template for production APIs.

---

## 🚀 Tech Stack

- **Python** ≥ 3.13  
- **FastAPI** — API framework  
- **Pydantic** — request/response validation  
- **Uvicorn** — ASGI server  
- **pytest** — testing framework  

---

## 📂 Project Structure

```
task-management-api/
├── src/
│   ├── main.py                # Application entry point
│   ├── api/
│   │   └── endpoints/
│   │       └── task.py        # Task endpoints (CRUD)
│   ├── models/
│   │   └── task.py            # Task domain model & in-memory storage
│   ├── schemas/
│   │   └── task.py            # Pydantic schemas for validation
│   └── services/
│       └── task_services.py   # Business logic for tasks
├── tests/                     # Unit & integration tests                   
├── .gitignore
├── .python-version
├── README.md
├── pyproject.toml             # Project metadata & dependencies
└── uv.lock                    # Lock file for dependencies
```

---

## ⚡ Installation & Running Locally

1. Clone the repository:
   ```bash
   git clone https://github.com/Prince-Letsyo/task-management-api.git
   cd task-management-api
   ```

2. Install dependencies:
   ```bash
   pip install .
   ```
   *(or use `pip install -r requirements.txt` if you generate one)*

3. Run the server:
   ```bash
   uvicorn src.main:app --reload
   ```

4. Access the app:
   - Swagger UI: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - ReDoc: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints

| Method | Endpoint        | Description              | Body Parameters |
|--------|----------------|--------------------------|----------------|
| GET    | `/tasks`       | Get all tasks            | — |
| GET    | `/tasks/{id}`  | Get a task by ID         | — |
| POST   | `/tasks`       | Create a new task        | `title` (str), `description` (str, optional), `due_date` (date) |
| PUT    | `/tasks/{id}`  | Update a task completely | same as `POST` |
| PATCH  | `/tasks/{id}`  | Partial update of a task | any subset of fields |
| DELETE | `/tasks/{id}`  | Delete a task            | — |

---

## 📝 Example Usage

**Create a task**
```bash
curl -X POST "http://127.0.0.1:8000/tasks"   -H "Content-Type: application/json"   -d '{"title":"Write docs","description":"Complete README","due_date":"2025-09-30"}'
```

**Update task (PATCH)**
```bash
curl -X PATCH "http://127.0.0.1:8000/tasks/1"   -H "Content-Type: application/json"   -d '{"title":"Write detailed docs"}'
```

**Delete task**
```bash
curl -X DELETE "http://127.0.0.1:8000/tasks/1"
```

---

## 🔍 Example Responses

**Task object**
```json
{
  "id": 1,
  "title": "Write docs",
  "description": "Complete README",
  "due_date": "2025-09-30"
}
```

**Error (task not found)**
```json
{
  "detail": "Task with id 42 not found"
}
```

---

## ✅ Running Tests

Run all tests with:
```bash
pytest
```

*(Tests cover services, schemas, and endpoints via FastAPI’s `TestClient`.)*

---

## 📌 Roadmap / Improvements

- [ ] Add persistent storage (SQLite / PostgreSQL)  
- [ ] Improve error handling & validation (e.g., ensure due date is future)  
- [ ] Authentication & authorization (user accounts, JWT, etc.)  
- [ ] Pagination & filtering for large task lists  
- [ ] Dockerize for deployment  
- [ ] CI/CD pipeline (GitHub Actions)  
- [ ] Expand test coverage  

---

## 🤝 Contributing

1. Fork the repo  
2. Create a feature branch (`git checkout -b feature-name`)  
3. Commit changes (`git commit -m "Added feature"`)  
4. Push to branch (`git push origin feature-name`)  
5. Open a Pull Request  

---

## 📜 License

This project is licensed under the **MIT License**.



from fastapi import FastAPI
from .api.endpoints import task_router



app = FastAPI(title="Task Management Api Project")
app.include_router(task_router, prefix="/api", tags=["tasks"])

@app.get("/")
def index():
    return {"message": "Welcome to Task Management Api Project!"}



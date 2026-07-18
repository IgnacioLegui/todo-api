from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from repository import PostgresTaskRepository

app = FastAPI(
    title="Task API",
    description="A simple CRUD API to manage a to-do list.",
    version="1.0"
)

repo = PostgresTaskRepository()

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
def root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    return repo.get_all()

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    task = repo.get_by_id(task_id)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    if not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    return repo.create(new_task.title)

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    if update.title is not None and not update.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")
    task = repo.update(task_id, update.title, update.done)
    if task is None:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
    return task

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    deleted = repo.delete(task_id)
    if not deleted:
        raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
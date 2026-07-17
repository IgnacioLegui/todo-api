from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional

app = FastAPI(
    title="Task API",
    description="A simple CRUD API to manage a to-do list.",
    version="1.0"
)

tasks = [
    {"id": 1, "title": "Buy milk and eggs", "done": True},
    {"id": 3, "title": "Finish CRUD assignment", "done": False},
]

class TaskCreate(BaseModel):
    title: str

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    done: Optional[bool] = None

@app.get("/")
def root():
    """Basic info about this API and its endpoints."""
    return {
        "name": "Task API",
        "version": "1.0",
        "endpoints": ["/tasks"]
    }

@app.get("/health")
def health():
    """Health check — confirms the server is alive."""
    return {"status": "ok"}

@app.get("/tasks")
def get_tasks():
    """Returns the full list of tasks."""
    return tasks

@app.get("/tasks/{task_id}")
def get_task(task_id: int):
    """Returns a single task by id, or 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.post("/tasks", status_code=201)
def create_task(new_task: TaskCreate):
    """Creates a new task. Title must not be empty."""
    if not new_task.title.strip():
        raise HTTPException(status_code=400, detail="Title cannot be empty")

    next_id = max((t["id"] for t in tasks), default=0) + 1
    task = {"id": next_id, "title": new_task.title, "done": False}
    tasks.append(task)
    return task

@app.put("/tasks/{task_id}")
def update_task(task_id: int, update: TaskUpdate):
    """Updates a task's title and/or done status. 404 if the id doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            if update.title is not None:
                if not update.title.strip():
                    raise HTTPException(status_code=400, detail="Title cannot be empty")
                task["title"] = update.title
            if update.done is not None:
                task["done"] = update.done
            return task
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    """Deletes a task by id. 404 if it doesn't exist."""
    for task in tasks:
        if task["id"] == task_id:
            tasks.remove(task)
            return
    raise HTTPException(status_code=404, detail=f"Task {task_id} not found")
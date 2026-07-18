from abc import ABC, abstractmethod
from typing import Optional
import os
import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

load_dotenv()


class TaskRepository(ABC):
    """Defines the interface both storage backends must implement.
    Routes depend on this, never on storage details."""

    @abstractmethod
    def get_all(self) -> list[dict]:
        ...

    @abstractmethod
    def get_by_id(self, task_id: int) -> Optional[dict]:
        ...

    @abstractmethod
    def create(self, title: str) -> dict:
        ...

    @abstractmethod
    def update(self, task_id: int, title: Optional[str], done: Optional[bool]) -> Optional[dict]:
        ...

    @abstractmethod
    def delete(self, task_id: int) -> bool:
        ...


class InMemoryTaskRepository(TaskRepository):
    """The original Week 2 implementation, kept as-is for comparison."""

    def __init__(self):
        self.tasks = [
            {"id": 1, "title": "Buy milk and eggs", "done": True},
            {"id": 3, "title": "Finish CRUD assignment", "done": False},
        ]

    def get_all(self):
        return self.tasks

    def get_by_id(self, task_id):
        for task in self.tasks:
            if task["id"] == task_id:
                return task
        return None

    def create(self, title):
        next_id = max((t["id"] for t in self.tasks), default=0) + 1
        task = {"id": next_id, "title": title, "done": False}
        self.tasks.append(task)
        return task

    def update(self, task_id, title, done):
        task = self.get_by_id(task_id)
        if task is None:
            return None
        if title is not None:
            task["title"] = title
        if done is not None:
            task["done"] = done
        return task

    def delete(self, task_id):
        task = self.get_by_id(task_id)
        if task is None:
            return False
        self.tasks.remove(task)
        return True


class PostgresTaskRepository(TaskRepository):
    """Real persistence, backed by the tasks table in Postgres."""

    def __init__(self):
        self.dsn = os.environ["DATABASE_URL"]

    def _connect(self):
        return psycopg2.connect(self.dsn, cursor_factory=psycopg2.extras.RealDictCursor)

    def get_all(self):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks ORDER BY id")
            return cur.fetchall()

    def get_by_id(self, task_id):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("SELECT id, title, done FROM tasks WHERE id = %s", (task_id,))
            return cur.fetchone()

    def create(self, title):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "INSERT INTO tasks (title) VALUES (%s) RETURNING id, title, done",
                (title,),
            )
            return cur.fetchone()

    def update(self, task_id, title, done):
        existing = self.get_by_id(task_id)
        if existing is None:
            return None
        new_title = title if title is not None else existing["title"]
        new_done = done if done is not None else existing["done"]
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute(
                "UPDATE tasks SET title = %s, done = %s WHERE id = %s RETURNING id, title, done",
                (new_title, new_done, task_id),
            )
            return cur.fetchone()

    def delete(self, task_id):
        with self._connect() as conn, conn.cursor() as cur:
            cur.execute("DELETE FROM tasks WHERE id = %s", (task_id,))
            return cur.rowcount > 0
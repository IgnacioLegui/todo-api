# Task API

A simple CRUD API to manage a to-do list, built with FastAPI. Data is stored in memory (no database) and resets when the server restarts.

## How to run

1. Clone this repo and enter the folder
2. Create and activate a virtual environment:
```
   python -m venv venv
   venv\Scripts\activate
```
3. Install dependencies:
```
   pip install fastapi uvicorn
```
4. Start the server:
```
   uvicorn main:app --reload
```
5. Open `http://localhost:8000/docs` to explore the API

## Endpoints

| Method | Path | Description |
|---|---|---|
| GET | / | Basic info about the API |
| GET | /health | Health check |
| GET | /tasks | List all tasks |
| GET | /tasks/{id} | Get a single task |
| POST | /tasks | Create a new task |
| PUT | /tasks/{id} | Update a task |
| DELETE | /tasks/{id} | Delete a task |

## Example request

```
HTTP/1.1 200 OK
date: Fri, 17 Jul 2026 22:44:36 GMT
server: uvicorn
content-length: 105
content-type: application/json

[{"id":1,"title":"Buy milk and eggs","done":true},{"id":3,"title":"Finish CRUD assignment","done":false}]
```

## Swagger UI

![Swagger UI](screenshots/swagger.png)

All endpoints are documented and testable at `/docs`.
from fastapi import FastAPI
from celery.result import AsyncResult
from tasks import process_task

app = FastAPI()

@app.post("/submit-task/")
def submit_task(x: int, y: int):
    task = process_task.delay(x, y)
    return {"task_id": task.id, "status": "Task Submitted"}

@app.get("/task-status/{task_id}")
def task_status(task_id: str):
    task_result = AsyncResult(task_id)
    return {"task_id": task_id, "status": task_result.state, "result": task_result.result}

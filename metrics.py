from fastapi import FastAPI
from prometheus_client import Counter, generate_latest

app = FastAPI()

task_counter = Counter("task_counter", "Number of tasks processed")

@app.get("/metrics")
def get_metrics():
    return generate_latest()

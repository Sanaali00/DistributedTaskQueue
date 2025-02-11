from celery import Celery
from kombu import Exchange, Queue

# Initialize Celery with the correct broker URL
app = Celery(
    "tasks",
    broker="pyamqp://guest@localhost//",  # Corrected broker URL
    backend="rpc://"
)

# Configure task queues
app.conf.task_queues = (
    Queue("high_priority", Exchange("high"), routing_key="high"),
    Queue("low_priority", Exchange("low"), routing_key="low"),
)

# High priority task
@app.task(queue="high_priority")
def high_priority_task():
    return "High Priority Task Executed"

# Process task with retries
@app.task(bind=True, autoretry_for=(Exception,), retry_backoff=5, retry_kwargs={"max_retries": 3}, queue="low_priority")
def process_task(self, x, y):
    if x == 0:
        raise ValueError("x cannot be zero!")
    return x + y
from tasks import process_task

result = process_task.delay(5, 3)
print(result.get())

app.conf.broker_connection_retry_on_startup = True

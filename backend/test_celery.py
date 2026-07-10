# from config.celery import app

# result = app.send_task(
#     "apps.users.tasks.email.send_email_verification_email",
#     kwargs={
#         "recipient": "john@example.com",
#         "full_name": "John",
#         "verification_url": "https://google.com",
#     },
# )

# print(result.id)

from celery import Celery

app = Celery(
    "test",
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/1",
)

@app.task
def hello():
    print("HELLO TASK EXECUTED")
    return "hello"
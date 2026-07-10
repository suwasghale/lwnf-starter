from celery import shared_task


@shared_task
def hello():
    print("=" * 50)
    print("HELLO FROM CELERY")
    print("=" * 50)
    return "OK"
from celery_app import celery

@celery.task
def test_task():
    return "Task de teste executada com sucesso!" 
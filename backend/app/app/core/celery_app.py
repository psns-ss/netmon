from celery import Celery

celery_app = Celery("worker", broker="amqp://guest@queue//")

celery_app.conf.task_routes = {
    "app.worker.test_celery": "main-queue",
    "app.worker.check_machines_statuses": "main-queue",
}

celery_app.conf.beat_schedule = {
    "check-machines-periodically": {
        "task": "app.worker.check_machines_statuses",
        "schedule": 30.0,
    },
}

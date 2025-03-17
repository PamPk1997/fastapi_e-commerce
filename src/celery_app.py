from celery import Celery

CELERY_BROKER_URL = "redis://redis:6379/0"
CELERY_RESULT_BACKEND = "redis://redis:6379/0"


celery_app = Celery(
    "ecom",
    broker = CELERY_BROKER_URL,
    backend= CELERY_RESULT_BACKEND,
)

celery_app.conf.update(
    task_serializer = "json",
    accept_content=["json"],
    resul_expires=3600,

)
from celery import Celery

celery = Celery('worker', broker="redis://localhost:6379/0")

from app.worker import tasks

# celery -A app.worker.celery_app worker --loglevel=info --pool=solo
import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nas_ss.settings')
app = Celery('nas_celery_work')
app.config_from_object('django.conf:settings')

app.autodiscover_tasks()

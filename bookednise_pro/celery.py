import os
from celery import Celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bookednise_pro.settings')
app = Celery('bookednise_pro')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()
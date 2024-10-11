from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Set default Django settings module for Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'job_scraper_app.settings')

# Initialize the Celery application
app = Celery('job_scraper_app')

# Load task modules from all registered Django apps
app.config_from_object('django.conf:settings', namespace='CELERY')

# Autodiscover tasks in Django apps
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')

app.conf.worker_pool = 'solo'

app.conf.task_send_sent_event = True
app.conf.worker_send_task_events = True

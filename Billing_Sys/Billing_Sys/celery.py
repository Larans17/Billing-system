# # celery.py
# import os
# from celery import Celery

# from celery.schedules import crontab
# from django_celery_beat.models import PeriodicTask, IntervalSchedule


# os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Billing_Sys.settings")

# app = Celery("Billing_Sys")
# app.config_from_object("django.conf:settings", namespace="CELERY")

# # Auto-discover tasks in installed Django apps
# app.autodiscover_tasks()




# coding:utf-8
import os

from celery import Celery
from django.conf import settings

project_name = os.path.split(os.path.abspath('.'))[-1]
project_settings = '{0}.settings'.format(project_name)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', project_settings)

app = Celery(project_name)

app.config_from_object('django.conf:settings')

app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

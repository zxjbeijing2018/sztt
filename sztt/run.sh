#!/bin/bash
setsid celery -A sztt worker -l info
setsid python3 manage.py runserver 0.0.0.0:8070
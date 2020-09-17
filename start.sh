# !/bin/bash
python manage.py collectstatic --noinput &&
python manage.py makemigrations &&
python manage.py migrate &&
gunicorn main.asgi:application  -w 4 -k uvicorn.workers.UvicornWorker

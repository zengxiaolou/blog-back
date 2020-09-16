# !/bin/bash

python manage.py collectstatic --noinput &&
python manage.py makemigrations &&
python manage.py migrate &&
python search_index --rebuild &&
uvicorn main..wsgi:application -c gunicorn.conf

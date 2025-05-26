#!/bin/bash

./wait-for-it.sh db:3306 --timeout=60 --strict -- echo "Database is up"

python manage.py makemigrations
python manage.py migrate
python manage.py load_sql
python manage.py collectstatic --noinput

echo "from django.contrib.auth import get_user_model; \
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin123')
" | python manage.py shell

exec gunicorn --bind 0.0.0.0:3000 altflex.wsgi:application
#!/bin/bash
set -e

# Aguarda Banco subir
./wait-for-it.sh db:3306 --timeout=60 --strict -- echo "Database is up"

# Realiza migrations e coleta os estáticos
echo "Aplicando migrações..."
python manage.py migrate
echo "Coletando arquivos estáticos..."
python manage.py collectstatic --noinput --clear

# Cria o superusuário se não existir
echo "from django.contrib.auth import get_user_model; \
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin123')
" | python manage.py shell

# Importa os dados dos fixtures na ordem correta
echo "Importando fixtures..."
python manage.py loaddata dump/accounts_bkp_utf8.json
python manage.py loaddata dump/logistic_bkp_utf8.json
python manage.py loaddata dump/common_bkp_utf8.json
python manage.py loaddata dump/products_bkp_utf8.json
python manage.py loaddata dump/transactions_bkp_utf8.json

echo "Fixtures importadas com sucesso."

# Inicia o servidor Gunicorn
exec gunicorn --bind 0.0.0.0:3000 altflex.wsgi:application
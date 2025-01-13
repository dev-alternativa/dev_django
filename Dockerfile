# Use uma imagem base oficial do Python (versão slim)
FROM python:3.12.3-slim

# Define o diretório de trabalho
WORKDIR /app_alternativa

# Instala as dependências necessárias para build (compilação de pacotes)
RUN apt-get update && apt-get install -y --no-install-recommends \
        pkg-config \
        python3-dev \
        default-mysql-client \
        build-essential \
        default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar dependências do Python
COPY requirements.txt /app_alternativa
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . /app_alternativa/

# Configurar arquivos estáticos
RUN python manage.py collectstatic --no-input

# Criar usuário não-root e configurar como usuário padrão
RUN adduser --disabled-password --gecos '' django_user && \
    chown -R django_user:django_user /app_alternativa

# Trocar para o usuário não-root
USER django_user

# Expor porta para o Gunicorn
EXPOSE 8080

# Definir a porta padrão como 8000 se não estiver definida
ENV PORT=8000

# Criar um script de entrada
RUN echo '#!/bin/bash\n\
exec gunicorn --bind 0.0.0.0:${PORT:-8000} altflex.wsgi:application' > /app_alternativa/entrypoint.sh && \
    chmod +x /app_alternativa/entrypoint.sh

CMD ["/app_alternativa/entrypoint.sh"]

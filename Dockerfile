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

# Copia Script para o container
COPY wait-for-it.sh /app_alternativa

# Atribui permissão de execução ao script
RUN chmod +x /app_alternativa/wait-for-it.sh

# Copiar o código da aplicação
COPY . .

# Coleta  arquivos estáticos
RUN python manage.py collectstatic --no-input

# Expor porta para o Gunicorn
EXPOSE 8080

# Executa servidor (Gunicorn) na porta 8080
CMD ["gunicorn", "altflex.wsgi:application", "--bind", "0.0.0.0:8000"]
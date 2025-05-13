# Imagem base oficial do Python (versão slim)
FROM python:3.12.3-slim

# Define o diretório de trabalho
WORKDIR /app_alternativa

# Variável de ambiente para evitar prompts interativos
ENV DEBIAN_FRONTEND=noninteractive


# Instala as dependências necessárias para build (compilação de pacotes)
RUN apt-get update && apt-get install -y --no-install-recommends \
        curl \
        gcc \
        default-libmysqlclient-dev \
        libmariadb-dev \
        build-essential \
        pkg-config \
        python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copia Script para o container
COPY wait-for-it.sh /app_alternativa

# Atribui permissão de execução ao script
RUN chmod +x /app_alternativa/wait-for-it.sh

# Instalar dependências do Python
COPY requirements.txt /app_alternativa
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Coleta  arquivos estáticos
RUN python manage.py collectstatic --no-input

# Expor porta para o Gunicorn
EXPOSE 3000

# Executa servidor (Gunicorn) na porta 8080
CMD ["gunicorn", "altflex.wsgi:application", "--bind", "0.0.0.0:3000"]
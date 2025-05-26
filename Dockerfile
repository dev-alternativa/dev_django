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
        build-essential \
        default-libmysqlclient-dev \
        libmariadb-dev \
        pkg-config \
        python3-dev \
        libpango-1.0-0 \
        libpangocairo-1.0-0 \
        libcairo2 \
        libgdk-pixbuf2.0-0 \
        libffi-dev \
        libjpeg-dev \
        libopenjp2-7-dev \
        libglib2.0-0 \
        shared-mime-info \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Instalar dependências do Python
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copiar o código da aplicação
COPY . .

# Atribui permissão de execução ao script
RUN chmod +x ./wait-for-it.sh ./entrypoint.sh

# Expor porta para o Gunicorn
EXPOSE 3000

ENTRYPOINT ["./entrypoint.sh"]
# Use uma imagem base oficial do Python
FROM python:3.12.3

# Define o diretório de trabalho dentro do contêiner
WORKDIR /usr/src/app_alternativa

# Copie o arquivo de requisitos e instale as dependências
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copie o código do projeto para o diretório de trabalho
COPY . .

# Instala o cliente MySQL (se necessário para testes)
RUN apt-get update && apt-get install -y default-mysql-client


# Expõe a porta que o Django usa (por padrão é 8000)
EXPOSE 8001

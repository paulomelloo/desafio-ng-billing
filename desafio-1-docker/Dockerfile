FROM python:3.11-slim

WORKDIR /usr/src/app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY app.py .

# Define o diretório que será o ponto de montagem (o diretório a ser lido)
ENV FILE_DIRECTORY=/data/files

# Cria o diretório (se não existir) para garantir permissões
RUN mkdir -p ${FILE_DIRECTORY}

EXPOSE 5000

# Usaremos Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "app:app"]
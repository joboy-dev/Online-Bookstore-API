FROM python:3.11.9-slim-bullseye

WORKDIR /app

# Install all dependencies 
RUN apt-get update

# Copy requirements.txt file
COPY requirements.txt /app/requirements.txt

# Copy all needed files to docker image app folder
COPY . /app/

# Use Docker secrets for sensitive files
# Note: The secrets are made available by Docker Compose
RUN --mount=type=secret,id=firebase_config,target=/app/secret/firebase_config.py \
    --mount=type=secret,id=service_account,target=/app/secret/serviceAccount.json \
    true

ENV PYTHONPATH=/app

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt
# RUN flask db migrate -m "Make db migrations"
RUN flask db upgrade

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8080

CMD [ "python", "app.py" ]
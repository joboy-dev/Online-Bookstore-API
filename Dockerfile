FROM python:3.11.9-slim-bullseye

WORKDIR /app

# Install all dependencies 
RUN apt-get update

# Copy all needed files to docker image app folder
COPY . /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
# RUN flask db migrate -m "Make db migrations"

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

EXPOSE 8080

CMD [ "python", "app.py" ]
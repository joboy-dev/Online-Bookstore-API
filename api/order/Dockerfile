FROM python:3.11.9-slim-bullseye

WORKDIR /app/api/order

# Install all dependencies 
RUN apt-get update

# Copy all needed files to docker image app/order folder
COPY . /app/order/

RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

CMD [ "python", "app.py" ]
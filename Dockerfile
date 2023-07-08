FROM docker.io/python:3.11.3

ENV PYTHONUNBUFFERED 1 \
    PYTHONDONTWRITEBYTECODE 1

WORKDIR /code/
COPY requirements.txt /code/
RUN pip install --upgrade pip \
    install -r requirements.txt
COPY . /code/

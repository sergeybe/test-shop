FROM python:3.8.5-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app/

COPY requirements.txt .
RUN pip install -r requirements.txt --no-cache-dir

COPY ./src/ .

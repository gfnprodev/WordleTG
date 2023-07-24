FROM python:3.11-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PYTHONPATH="${PYTHONPATH}:/src"

WORKDIR /src

COPY . /src

RUN python -m pip install --upgrade pip && python -m pip install --requirement requirements.txt

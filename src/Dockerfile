FROM python:3.8-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PROJECT_ROOT="/src"
ENV PYTHONPATH=${PYTHONPATH}:${PROJECT_ROOT}

ENV DEBIAN_FRONTEND noninteractive
RUN apt-get update && \
    apt-get -y install gcc && \
    rm -rf /var/lib/apt/lists/*

WORKDIR ${PROJECT_ROOT}

RUN pip install --no-cache-dir --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . ${PROJECT_ROOT}

EXPOSE 8080
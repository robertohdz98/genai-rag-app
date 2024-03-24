FROM python:3.10-slim-bullseye

RUN apt-get update --fix-missing
RUN apt-get install -y make curl vim wget

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
ENV PYTHONPATH=$PYTHONPATH:/app

RUN pip install --no-cache-dir --upgrade pip
RUN pip install poetry

COPY poetry.lock poetry.lock
COPY pyproject.toml pyproject.toml
COPY . $HOMEDIR

RUN poetry config virtualenvs.create false && poetry install
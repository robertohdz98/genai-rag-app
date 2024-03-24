FROM python:3.10-bullseye

RUN apt-get update --fix-missing
RUN pip install  --no-cache-dir --upgrade pip
RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

COPY . .

RUN poetry config virtualenvs.create false && poetry install

ENTRYPOINT ["python", "src/backend.py"]

FROM python:3.10-bullseye

RUN apt-get update --fix-missing
RUN apt-get install -y poppler-utils tesseract-ocr
RUN pip install  --no-cache-dir --upgrade pip
RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

COPY . .

RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8000

ENTRYPOINT ["python", "src/backend.py"]

FROM python:3.10-bullseye

RUN apt-get update --fix-missing
RUN pip install  --no-cache-dir --upgrade pip

ENV HOMEDIR=/app
RUN mkdir -p $HOMEDIR

WORKDIR $HOMEDIR
ENV PYTHONPATH=$PYTHONPATH:/app

RUN pip install poetry

COPY pyproject.toml pyproject.toml
COPY poetry.lock poetry.lock

COPY . .

RUN poetry config virtualenvs.create false && poetry install

EXPOSE 8501

ENTRYPOINT ["streamlit", "run", "src/app.py", "--server.address=0.0.0.0"]

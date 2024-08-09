FROM python:3.11

ENV POETRY_VERSION=1.8.3 \
    POETRY_VIRTUALENVS_CREATE=false

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . .

RUN chmod +x ./infra/commands/api.sh
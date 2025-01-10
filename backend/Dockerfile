FROM python:3.12-slim AS base

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl build-essential \
    && curl -sSL https://install.python-poetry.org | python3 - \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /backend

ENV PATH="/root/.local/bin:$PATH" \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    PYTHONPATH="/" \
    ENV_TYPE=stable

WORKDIR /backend

COPY pyproject.toml poetry.lock* .

RUN poetry install --without=dev --no-root

COPY . .

ENV ENV_TYPE=stable

CMD ["poetry", "run", "python", "main.py"]
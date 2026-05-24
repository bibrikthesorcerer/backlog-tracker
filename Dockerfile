FROM python:3.12-bookworm AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN curl -SL https://install.python-poetry.org | python -

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry install --no-interaction --no-ansi --without dev

# runtime
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install --no-install-recommends -y libpq5

COPY --from=builder /usr/local/lib/python3.12 /usr/local/lib/python3.12
COPY --from=builder /usr/local/bin /usr/local/bin

COPY api/ api/
COPY conf/ conf/
COPY models_app/ models_app/

COPY gunicorn_config_docker.py .
COPY config.py .
COPY manage.py .
COPY startup.py .

EXPOSE 8000

CMD ["python", "startup.py"]
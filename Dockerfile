FROM python:3.12-slim AS builder

RUN apt-get update && apt-get install --no-install-recommends -y \
    curl \
    build-essential && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONUNBUFFERED=1 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_CREATE=false \
    POETRY_VERSION=2.4.1

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN curl -SL https://install.python-poetry.org | python - --version $POETRY_VERSION

ENV PATH="$POETRY_HOME/bin:$PATH"

RUN poetry install --no-interaction --no-ansi --without dev

COPY --link api/ api/
COPY --link conf/ conf/
COPY --link models_app/ models_app/

COPY --link settings.toml .
COPY --link gunicorn_config_docker.py .
COPY --link config.py .
COPY --link manage.py .
COPY --link startup.py .

ENV BL_DJANGO__SECRET_KEY="dummy-key" \
    BL_EMAIL__USER="" \
    BL_EMAIL__PASSWORD=""

RUN python manage.py collectstatic --noinput

# runtime
FROM python:3.12-slim AS runtime

ENV PYTHONUNBUFFERED=1

WORKDIR /app

RUN useradd -r -u 1001 backlog && \
    mkdir -p /var/run/celery && \
    chown -R backlog:backlog /var/run/celery

USER backlog

COPY --from=builder /usr/local/lib/python3.12/site-packages /usr/local/lib/python3.12/site-packages
COPY --from=builder --chown=backlog:backlog /app /app

EXPOSE 8000

CMD ["python", "startup.py"]
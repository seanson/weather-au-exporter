FROM python:3.12-alpine AS base

ENV PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PYTHONUNBUFFERED=1

WORKDIR /app

FROM base AS builder

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

COPY pyproject.toml uv.lock ./
RUN uv sync --frozen --no-dev --no-install-project

COPY . .
RUN uv sync --frozen --no-dev

FROM base AS final

RUN apk add --no-cache tzdata
COPY --from=builder /app/.venv /venv
COPY docker-entrypoint.sh weather_au_exporter ./

ENV TZ=Australia/Sydney
CMD ["./docker-entrypoint.sh"]

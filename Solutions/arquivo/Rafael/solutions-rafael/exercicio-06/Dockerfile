FROM python:3.13-slim

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

WORKDIR /srv
ENV UV_COMPILE_BYTECODE=1 PYTHONUNBUFFERED=1

COPY pyproject.toml uv.lock* ./
RUN uv sync --no-dev

COPY pipeline pipeline
COPY main.py ./
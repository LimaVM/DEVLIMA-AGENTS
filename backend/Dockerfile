FROM python:3.12-slim@sha256:f77ac9e44ae96ef2c90b8053ea08c31f8be030f824196b0ae4db6d462c84e51f AS base
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1 PIP_NO_CACHE_DIR=1
WORKDIR /app
COPY requirements.txt .
RUN pip install --disable-pip-version-check -r requirements.txt
RUN groupadd --gid 10001 agent && useradd --uid 10001 --gid agent --no-create-home agent
COPY app ./app
COPY alembic.ini .
COPY migrations ./migrations
USER 10001:10001
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--ws", "websockets-sansio", "--ws-max-size", "65536", "--limit-concurrency", "128", "--proxy-headers", "--forwarded-allow-ips", "*"]

FROM base AS test
USER root
COPY requirements-dev.txt pyproject.toml ./
RUN pip install --disable-pip-version-check -r requirements-dev.txt
COPY tests ./tests
USER 10001:10001
CMD ["pytest", "-q", "-p", "no:cacheprovider"]

FROM base AS production

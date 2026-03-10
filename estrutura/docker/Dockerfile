# syntax=docker/dockerfile:1.7
# Dockerfile da Aula 4 alinhado ao projeto Django + DRF existente.
# Contexto esperado de build: pasta `estrutura/`.

ARG PYTHON_VERSION=3.12-slim
ARG APP_USER=app

FROM python:${PYTHON_VERSION} AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /src

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Copia dependencias primeiro para aproveitar cache de build.
COPY requirements.txt ./requirements.txt

RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:${PATH}"

RUN --mount=type=cache,target=/root/.cache/pip \
    python -m pip install --upgrade pip \
    && pip install -r requirements.txt

FROM python:${PYTHON_VERSION} AS runtime
ARG APP_USER=app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    DJANGO_SETTINGS_MODULE=config.settings \
    PATH="/opt/venv/bin:${PATH}"

WORKDIR /app

RUN groupadd --system ${APP_USER} \
    && useradd --system --create-home --gid ${APP_USER} ${APP_USER}

COPY --from=builder /opt/venv /opt/venv
COPY --chown=${APP_USER}:${APP_USER} . /app/
RUN mkdir -p /app/staticfiles \
    && chown -R ${APP_USER}:${APP_USER} /app

USER ${APP_USER}

EXPOSE 8000

HEALTHCHECK --interval=30s --timeout=3s --start-period=20s --retries=3 \
    CMD python -c "import socket; s=socket.socket(); s.settimeout(2); s.connect(('127.0.0.1', 8000)); s.close()" || exit 1

# Aplica migracoes com retry e sobe o servidor WSGI da aplicacao DRF.
CMD ["sh", "docker/entrypoint.sh"]

ARG PYTHON_VERSION=3.10.7-slim-bullseye

# define an alias for the specfic python version used in this file.
FROM python:${PYTHON_VERSION} as python

# Python build stage
FROM python as python-build-stage

ARG BUILD_ENVIRONMENT=local

# Python 'run' stage
FROM python as python-run-stage

ARG BUILD_ENVIRONMENT=local
ARG APP_HOME=/app

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    \
    # poetry
    POETRY_VERSION=1.2.2 \
    POETRY_HOME="/opt/poetry" \
    POETRY_VIRTUALENVS_IN_PROJECT=false \
    POETRY_NO_INTERACTION=1

ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

# Install essentials
RUN apt update \
    && apt install --no-install-recommends -y \
        git \
        curl \
        libpq-dev \
        build-essential
RUN apt install --no-install-recommends -y fonts-dejavu-core fonts-dejavu-extra

COPY ./docker/scripts/get-poetry.py /tmp/get-poetry.py
RUN python /tmp/get-poetry.py

WORKDIR ${APP_HOME}
COPY . ${APP_HOME}

RUN poetry config virtualenvs.create false
RUN poetry install --only main

# Cleanup installation
RUN apt remove -y build-essential
RUN apt autoremove -y
RUN rm -rf /var/lib/apt/lists/*
RUN rm /tmp/get-poetry.py

COPY ./docker/local/bot/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint

COPY ./docker/local/bot/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start

ARG user=tuxbot
ARG group=tuxbot
ARG uid=1000
ARG gid=1000
RUN groupadd -g ${gid} ${group}
RUN useradd -u ${uid} -g ${group} -s /bin/nologin -m ${user}

RUN chown ${user}:${group} -R ${APP_HOME}
USER ${user}:${group}

RUN poetry config virtualenvs.create false

ENTRYPOINT ["/entrypoint"]

FROM node:10-stretch-slim as client-builder

WORKDIR /app

# Python build stage
FROM python:3.9-slim-buster

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

RUN addgroup --system tuxbot \
    && adduser --system --ingroup tuxbot tuxbot

# Requirements are installed here to ensure they will be cached.
COPY --chown=tuxbot:tuxbot ./compose/production/tuxbot/entrypoint /entrypoint
RUN sed -i 's/\r$//g' /entrypoint
RUN chmod +x /entrypoint


COPY --chown=tuxbot:tuxbot ./compose/production/tuxbot/start /start
RUN sed -i 's/\r$//g' /start
RUN chmod +x /start
COPY --from=client-builder --chown=tuxbot:tuxbot /app /app


USER tuxbot

WORKDIR /app

ENTRYPOINT ["/entrypoint"]

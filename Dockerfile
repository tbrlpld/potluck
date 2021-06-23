FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN useradd -m potluck -s /bin/bash && \
    chown -R potluck /app
USER potluck

ENV POETRY_HOME=/home/potluck/poetry

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=${POETRY_HOME}/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=potluck.settings.base
RUN env

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

COPY --chown=potluck:potluck . .

EXPOSE 8000
# CMD poetry run gunicorn potluck.wsgi:application -b 0:8000
CMD tail -f /dev/null

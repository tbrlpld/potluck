FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN useradd -m potluck -s /bin/bash
USER potluck

ARG POETRY_HOME=/home/potluck/poetry

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH=${POETRY_HOME}/bin:$PATH
ENV DJANGO_SETTINGS_MODULE=potluck.settings.base
RUN env

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install

COPY . .

EXPOSE 8000
CMD poetry run python manage.py migrate --noinput; \
    poetry run gunicorn potluck.wsgi:application -b 0:8000

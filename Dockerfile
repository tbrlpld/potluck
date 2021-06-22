FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN useradd -m potluck -s /bin/bash
USER potluck

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV POETRY /home/potluck/.poetry/bin/poetry
RUN env

COPY pyproject.toml .
COPY poetry.lock .

RUN $POETRY install

COPY . .

EXPOSE 8000
CMD $POETRY run python manage.py migrate --noinput; \
    $POETRY run gunicorn potluck.wsgi:application -b 0:8000
    # python manage.py runserver 0:8000


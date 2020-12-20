FROM python:3.8

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV POETRY=/root/.poetry/bin/poetry

RUN mkdir /app
WORKDIR /app
COPY pyproject.toml .
COPY poetry.lock .

RUN $POETRY install

COPY . .

RUN $POETRY run python manage.py migrate

EXPOSE 8000
CMD $POETRY run python manage.py runserver 0:8000

FROM node:14 as frontend

COPY package.json package-lock.json ./
RUN npm ci --no-optional --no-audit --progress=false

# The whole project is needed to allow purging of the unused CSS classes.
COPY . .
# Compile static files
RUN npm run build:css

FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN useradd -m potluck -s /bin/bash && \
    chown -R potluck /app

ENV POETRY_HOME=/home/potluck/poetry
ENV PATH=${POETRY_HOME}/bin:$PATH \
    # Ensure dependencies are available globally (without having to mess with the poetry's venvs)
    POETRY_VIRTUALENVS_CREATE=false \
    DJANGO_SETTINGS_MODULE=potluck.settings.base
RUN env

# Install poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN chown -R potluck:potluck ${POETRY_HOME}

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root --no-interaction --no-ansi

USER potluck

COPY --chown=potluck:potluck . .

COPY --chown=potluck:potluck --from=frontend ./potluck/static/dist ./potluck/static/dist

RUN ./manage.py collectstatic --noinput

EXPOSE 8000
CMD gunicorn --bind 0.0.0.0:$PORT potluck.wsgi:application

FROM python:3.9

RUN mkdir /app
WORKDIR /app
RUN useradd -m potluck -s /bin/bash && \
    chown -R potluck /app

# Install poetry
ENV POETRY_HOME=/home/potluck/poetry \
    # Ensure dependencies are available globally (without having to mess with the poetry's venvs)
    POETRY_VIRTUALENVS_CREATE=false
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
RUN chown -R potluck:potluck ${POETRY_HOME}
ENV PATH=${POETRY_HOME}/bin:$PATH

ENV DJANGO_SETTINGS_MODULE=potluck.settings.base \
    # Port for Heroku (it ignores the EXPOSE) and Gunicorn
    PORT=8000 \
    # Concurrency for Gunicorn
    WEB_CONCURRENCY=3
RUN env

COPY pyproject.toml .
COPY poetry.lock .

RUN poetry install --no-root

USER potluck

COPY --chown=potluck:potluck . .

EXPOSE 8000
CMD gunicorn potluck.wsgi:application

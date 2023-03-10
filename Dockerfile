FROM python:3.9
ARG ENV_FOR_DYNACONF


WORKDIR /app

# Code
COPY pyproject.toml /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}
ENV PYTHONDONTWRITEBYTECODE=1

# PYTHON ENV
RUN pip3 install poetry==1.2.0
RUN poetry config virtualenvs.create false
RUN poetry install $(test "$ENV_FOR_DYNACONF" == production && echo "--no-dev") --no-interaction --no-ansi

COPY . /app

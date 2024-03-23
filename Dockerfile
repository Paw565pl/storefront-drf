FROM python:3.12-alpine

ENV POETRY_VIRTUALENVS_CREATE=false \
  POETRY_HOME='/usr/local' \
  POETRY_VERSION=1.8.2

RUN apk add curl gcc python3-dev musl-dev linux-headers
RUN curl -sSL https://install.python-poetry.org | python3 -

WORKDIR /app

COPY poetry.lock pyproject.toml ./

RUN poetry install --all-extras --compile

COPY . .

CMD sh -c "python manage.py migrate && python manage.py runserver 0.0.0.0:8000"

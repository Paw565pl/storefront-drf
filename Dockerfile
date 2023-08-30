FROM python:3.11.5-alpine3.18

RUN adduser -S backend
RUN addgroup backend && addgroup backend backend

WORKDIR /backend

RUN apk add --no-cache libpq-dev gcc python3-dev musl-dev linux-headers
RUN pip install --upgrade pip

COPY requirements.txt ./

RUN pip install -r requirements.txt --cache-dir=/tmp/pip-cache

COPY . .

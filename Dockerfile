FROM python:3.9-alpine

ENV TZ=Asia/Yekaterinburg

RUN apk update && apk add --virtual \
    build-deps \
    gcc \
    g++ \
    linux-headers \
    python3-dev \
    musl-dev \
    git

RUN pip3 install --upgrade pip

WORKDIR /opt

COPY ./src .

RUN pip3.9 install \
    --requirement requirements.txt \
    --no-cache-dir

ENV PYTHONPATH=/opt

WORKDIR /opt/src/database/migrations

RUN alembic upgrade head

WORKDIR /opt

ENTRYPOINT python3 run.py
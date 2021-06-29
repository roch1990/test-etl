FROM python:3.9-alpine

ENV TZ=Asia/Yekaterinburg

RUN apk add --virtual \
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

RUN pip3.7 install \
    --requirement requirements.txt \
    --no-cache-dir

EXPOSE 8080

ENTRYPOINT python3 run.py
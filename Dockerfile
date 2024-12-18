FROM python:3.12-bullseye AS base


RUN apt-get update -y && \
    pip install --upgrade pip

EXPOSE 8000

FROM base AS development

RUN apt-get update -y && \
    apt-get install -y \
    postgresql-client


FROM base AS production

RUN mkdir /workspace && \
    mkdir /workspace/src

COPY ./src /workspace/src

RUN pip install /workspace/src/
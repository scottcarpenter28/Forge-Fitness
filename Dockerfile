FROM python:3.12 AS base


RUN apt-get update -y \
    && pip install --upgrade pip

EXPOSE 8000

FROM base AS development

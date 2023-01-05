# syntax=docker/dockerfile:1

ARG PYTHON_TAG

FROM python:${PYTHON_TAG}

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/

WORKDIR /src

CMD python -m app

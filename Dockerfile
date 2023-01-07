# syntax=docker/dockerfile:1

ARG PYTHON_TAG

FROM python:${PYTHON_TAG}

RUN apt-get update && apt-get install -y gcc wget libmariadb3 libmariadb-dev
RUN wget https://dlm.mariadb.com/2678579/Connectors/c/connector-c-3.3.3/mariadb-connector-c-3.3.3-debian-buster-amd64.tar.gz -O - | tar -zxf - --strip-components=1 -C /usr

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p /src
COPY src/ /src/

WORKDIR /src

CMD python -m app

# syntax=docker/dockerfile:1

ARG PYTHON_TAG

FROM python:${PYTHON_TAG}

RUN apt-get update && apt-get install -y gcc curl wget
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup
RUN ./mariadb_repo_setup \ --mariadb-server-version="mariadb-10.6"
RUN apt install -y libmariadb3 libmariadb-dev

RUN pip install --upgrade pip

COPY requirements.txt /tmp/
RUN pip install -r /tmp/requirements.txt

RUN mkdir -p src json
COPY src/ /src/

WORKDIR /src

CMD python -m app
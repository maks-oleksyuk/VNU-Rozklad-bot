# syntax=docker/dockerfile:1

ARG PYTHON_TAG

FROM python:${PYTHON_TAG}

# Update and install the required packages.
RUN apt update && apt install -y gcc curl wget locales

# Download the installer for mariadb and run it.
RUN wget https://downloads.mariadb.com/MariaDB/mariadb_repo_setup
RUN chmod +x mariadb_repo_setup && ./mariadb_repo_setup
# Installing additional packages to fix bugs.
RUN apt install -y --no-install-recommends libmariadb3 libmariadb-dev

# Enable settings for Ukrainian localization.
RUN sed -i '/^#.* uk_UA.UTF-8 /s/^#//' /etc/locale.gen && locale-gen

# Update pip.
RUN pip install --upgrade pip

# Installing the python dependencies.
COPY requirements.txt /tmp/
RUN pip install --no-cache-dir -r  /tmp/requirements.txt && rm /tmp/requirements.txt

COPY . /usr/src/app

WORKDIR /usr/src/app

CMD python -m app

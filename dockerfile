# syntax=docker/dockerfile:1

# pull base image
FROM python:3.11-rc

# copy the dependencies file to the working directory
COPY requirements.txt ./app/

# set work directory
WORKDIR /app

# install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# сopy project
COPY . .

CMD ["python", "./bot.py"]

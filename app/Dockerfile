############################################################
# Dockerfile to build Python 3.6 WSGI Application Containers
############################################################

# Set the base image to Python 3.6
FROM python:3.6

MAINTAINER Stanislav WEB "stanisov@gmail.com"

COPY ./app /app

WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt
RUN chmod +x server.py

# Set the default command to execute
ENTRYPOINT ["/usr/local/bin/gunicorn", "--config", "./config.py", "server"]
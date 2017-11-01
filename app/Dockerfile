############################################################
# Dockerfile to build Python 3.6 WSGI Application Containers
############################################################

# Set the base image to Python 3.6
FROM python:3.6

MAINTAINER Stanislav WEB "stanisov@gmail.com"

COPY . /app

WORKDIR /app

# Install requirements
RUN pip install -r requirements.txt
RUN pip install -r requirements-dev.txt
RUN chmod +x server.py

EXPOSE 5000

# Set the default command to execute
ENTRYPOINT ["sh", "./entrypoint.sh"]
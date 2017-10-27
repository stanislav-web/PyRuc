#!/usr/bin/env bash

docker-compose down

fuser -k 5001/tcp
fuser -k 6379/tcp

docker rm $(docker stop $(docker ps -a -q --filter ancestor=pyrus --format="{{.ID}}"))
docker rm $(docker stop $(docker ps -a -q --filter ancestor=redis --format="{{.ID}}"))
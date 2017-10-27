#!/usr/bin/env bash

apidoc -i ./app/src/ -o ./apidoc --debug
surge ./apidoc/ -d drunk-start.surge.sh
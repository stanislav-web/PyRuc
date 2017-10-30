#!/usr/bin/env bash

APPLICATION="${APPLICATION}"
printf '\033[32m%s\n' "${APPLICATION}"

if [ $@ == '--reload' ]
then
    /usr/local/bin/gunicorn --config ./config.py server "$@"
else
    /usr/local/bin/coverage run setup.py test
    /usr/local/bin/coverage report
    /usr/local/bin/gunicorn --config ./config.py server
fi
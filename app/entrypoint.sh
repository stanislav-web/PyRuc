#!/usr/bin/env bash

APPLICATION="${APPLICATION}"
printf '\033[32m%s\n' "${APPLICATION}"

/usr/local/bin/coverage run setup.py test > /dev/null
/usr/local/bin/coverage report
/usr/local/bin/gunicorn --config ./config.py server


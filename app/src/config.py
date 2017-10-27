# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os

APPLICATION = os.getenv('APPLICATION', 'pyrus')
APPLICATION_LIMIT_REG = os.getenv('APPLICATION_LIMIT_REG', '100000 per day')
APPLICATION_LIMIT_AUTH = os.getenv('APPLICATION_LIMIT_AUTH', '100000 per day')
APPLICATION_LIMIT_RESTORE = os.getenv('APPLICATION_LIMIT_RESTORE', '100000 per day')
APPLICATION_LIMIT_PER_SEC = os.getenv('APPLICATION_LIMIT_PER_SEC', '100000 per second')
APPLICATION_LIMIT_PER_MIN = os.getenv('APPLICATION_LIMIT_PER_MIN', '100000 per minute')
APPLICATION_LIMIT_STORAGE_URI = os.getenv('APPLICATION_LIMIT_STORAGE_URI', 'redis://localhost:6379')

LOGSTASH_HOST = os.getenv('LOGSTASH_HOST', '127.0.0.1')
LOGSTASH_PORT = os.getenv('LOGSTASH_PORT', 6000)
LOGSTASH_INTERNAL_DB = os.getenv('LOGSTASH_INTERNAL_DB', './logs/log.db')

SERVER_HOST = os.getenv('SERVER_HOST', '0.0.0.0')
SERVER_PORT = int(os.getenv('SERVER_PORT', '5001'))
SERVER_DEBUG = os.getenv('SERVER_DEBUG', True)

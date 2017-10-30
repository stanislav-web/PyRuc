# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os
import redis
from redis.exceptions import RedisError
from ..interface import RepositoryInterface
from .exceptions import RedisRepositoryError


class RedisRepository(RepositoryInterface):
    """RedisRepository class"""

    REDIS_HOST = os.getenv('REDIS_HOST', '0.0.0.0')
    REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
    REDIS_DBNO = int(os.getenv('REDIS_DBNO', 2))
    REDIS_PASSWORD = os.getenv('REDIS_PASSWORD', None)
    REDIS_SOCKET_TIMEOUT = int(os.getenv('REDIS_SOCKET_TIMEOUT', 10))
    REDIS_SOCKET_CONNECT_TIMEOUT = int(os.getenv('REDIS_SOCKET_CONNECT_TIMEOUT', 3))
    REDIS_MAX_CONNECTIONS = int(os.getenv('REDIS_MAX_CONNECTIONS', 3))

    def __init__(self):
        """
        Init connection to RedisServer
        """

        super().__init__()

        try:
            self.db = redis.StrictRedis(host=self.REDIS_HOST,
                                        port=self.REDIS_PORT,
                                        db=self.REDIS_DBNO,
                                        password=self.REDIS_PASSWORD,
                                        socket_timeout=self.REDIS_SOCKET_TIMEOUT,
                                        socket_connect_timeout=self.REDIS_SOCKET_CONNECT_TIMEOUT,
                                        max_connections=self.REDIS_MAX_CONNECTIONS,
                                        decode_responses=True
                                        )
        except RedisError as error:
            raise RedisRepositoryError(error)

    def get_instance(self) -> redis.StrictRedis:
        """
        Get instance
        :return: redis.StrictRedis
        """

        return self.db

    def get_user(self, phone: str) -> dict:
        """
        Get user

        :param phone: str
        :return: dict
        """

        try:
            p = self.db.pipeline()
            user_id = self.db.get('phone:{phone}:id'.format(phone=phone))
            password_hash = self.db.get('phone:password_hash:{user_id}'.format(user_id=user_id))
            p.execute()

            return {} if None is password_hash else {
                'user_id': user_id,
                'password_hash': password_hash
            }
        except RedisError as error:
            raise RedisRepositoryError(error)

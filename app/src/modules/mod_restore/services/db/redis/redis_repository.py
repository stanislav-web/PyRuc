# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
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

    REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
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

    def add_restore_code(self, key: str, accept_code: int, ttl: int) -> str:
        """
        Add temporary restore code

        :param key: str
        :param accept_code: int
        :param ttl: int
        :return: str
        """

        try:
            key = '{key}:{suffix}'.format(key=key, suffix='restore')
            return self.db.setex(key, ttl, accept_code)
        except RedisError as error:
            raise RedisRepositoryError(error)

    def fetch_restore_code(self, key: str) -> str:
        """
        Fetch restore code by key

        :param key: str
        :return: str
        """

        try:
            key = '{key}:{suffix}'.format(key=key, suffix='restore')
            return self.db.get(key)
        except RedisError as error:
            raise RedisRepositoryError(error)

    def get_user_id(self, phone: str) -> int:
        """
        Get user identifier

        :param phone: str
        :return: int
        """

        try:
            user_id = self.db.get('phone:{phone}:id'.format(phone=phone))
            return int(user_id)
        except RedisError as error:
            raise RedisRepositoryError(error)

    def is_user_exist(self, phone) -> bool:
        """
        Check if user already exist

        :param phone:
        :return: bool
        """

        try:
            result = self.db.get('phone:{phone}:id'.format(phone=phone))
            return result is not None
        except RedisError as error:
            raise RedisRepositoryError(error)

    def update_user(self, user) -> None:
        """
        Update user

        :param user: User schema
        :return: None
        """

        try:
            p = self.db.pipeline()
            self.db.set('phone:password_hash:{id}'.format(id=user.get('user_id')), user.get('password_hash'))
            self.db.delete('{key}:{suffix}'.format(key=user.get('phone'), suffix='restore'))
            p.execute()

            return None

        except RedisError as error:
            raise RedisRepositoryError(error)

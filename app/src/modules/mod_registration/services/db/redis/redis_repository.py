# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
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

    def add_reg_code(self, key: str, accept_code: int, ttl: int) -> str:
        """
        Add temporary registration code

        :param key: str
        :param accept_code: int
        :param ttl: int
        :return: str
        """

        try:
            key = '{key}:{suffix}'.format(key=key, suffix='reg')
            return self.db.setex(key, ttl, accept_code)
        except RedisError as error:
            raise RedisRepositoryError(error)

    def fetch_reg_code(self, key: str) -> str:
        """
        Fetch registration code by key

        :param key: str
        :return: str
        """

        try:
            key = '{key}:{suffix}'.format(key=key, suffix='reg')
            return self.db.get(key)
        except RedisError as error:
            raise RedisRepositoryError(error)

    def is_user_exist(self, phone: str) -> bool:
        """
        Check if user already exist

        :param phone: str
        :return: bool
        """

        try:
            result = self.db.get('phone:{phone}:id'.format(phone=phone))
            return result is not None
        except RedisError as error:
            raise RedisRepositoryError(error)

    def create_user(self, user) -> int:
        """
        Create new user

        :param user: User schema
        :return: int
        """

        try:
            user_id = self.db.incr('global:nextUserId')
            p = self.db.pipeline()
            self.db.set('phone:{phone}:id'.format(phone=user.get('phone')), user_id)
            self.db.set('phone:password_hash:{id}'.format(id=user_id), user.get('password_hash'))
            self.db.set('phone:create_date:{id}'.format(id=user_id), user.get('create_date'))
            self.db.set('phone:is_active:{id}'.format(id=user_id), user.get('is_active'))
            self.db.delete('{key}:{suffix}'.format(key=user.get('phone'), suffix='reg'))
            self.db.sadd('global:users', user_id)
            p.execute()

            return user_id

        except RedisError as error:
            raise RedisRepositoryError(error)

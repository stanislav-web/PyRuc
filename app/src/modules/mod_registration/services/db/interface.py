# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


import abc


class RepositoryInterface(metaclass=abc.ABCMeta):
    """RepositoryInterface class"""

    def __init__(self):
        """
        Initialize interface
        """

        super(RepositoryInterface, self).__init__()

    @abc.abstractmethod
    def add_reg_code(self, key: str, accept_code: int, ttl: int) -> str:
        """
        Add temporary registration code

        :param key: str
        :param accept_code: int
        :param ttl: int
        :return: str
        """

        pass

    @abc.abstractmethod
    def fetch_reg_code(self, key: str) -> str:
        """
        Fetch registration code by key

        :param key: str
        :return: str
        """

        pass

    @abc.abstractmethod
    def is_user_exist(self, phone: str) -> bool:
        """
        Check if user already exist

        :param phone: str
        :return: bool
        """

        pass

    @abc.abstractmethod
    def create_user(self, user) -> int:
        """
        Create new user

        :param user: User schema
        :return: int
        """

        pass

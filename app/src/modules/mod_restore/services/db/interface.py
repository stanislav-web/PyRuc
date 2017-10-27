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
    def add_restore_code(self, key: str, accept_code: int, ttl: int) -> str:
        """
        Add temporary restore code

        :param key: str
        :param accept_code: int
        :param ttl: int
        :return: str
        """

        pass

    @abc.abstractmethod
    def fetch_restore_code(self, key: str) -> str:
        """
        Fetch restore code by key

        :param key: str
        :return: str
        """

        pass

    @abc.abstractmethod
    def get_user_id(self, phone: str) -> int:
        """
        Get user identifier

        :param phone: str
        :return: int
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
    def update_user(self, user) -> None:
        """
        Update user

        :param user: User schema
        :return: None
        """

        pass

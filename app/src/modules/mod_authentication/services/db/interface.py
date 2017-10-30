# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
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
    def get_instance(self):
        """
        Get instance
        :return: redis.StrictRedis
        """

        pass

    @abc.abstractmethod
    def get_user(self, phone: str) -> dict:
        """
        Get user

        :param phone: str
        :return: dict
        """

        pass

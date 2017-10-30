# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class User(object):
    """User class"""

    def __init__(self, phone: int, password: str):
        """
        Init user model

        :param phone: int
        :param password: str
        """

        self.phone = phone
        self.password = password

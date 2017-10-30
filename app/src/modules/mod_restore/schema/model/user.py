# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class User(object):
    """User class"""

    def __init__(self, user_id: int, phone: int, password_hash: str):
        """
        Init user model

        :param user_id: int
        :param phone: int
        :param password_hash: str
        """

        self.user_id = user_id
        self.phone = phone
        self.password_hash = password_hash

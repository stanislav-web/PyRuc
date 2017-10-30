# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import time


class User(object):
    """User class"""

    def __init__(self, phone: int, password_hash: str):
        """
        Init user model

        :param phone: int
        :param password_hash: str
        """

        self.phone = phone
        self.password_hash = password_hash
        self.create_date = time.time()
        self.is_active = False

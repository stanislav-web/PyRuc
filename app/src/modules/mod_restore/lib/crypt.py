# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import string
from random import randint, choice
import bcrypt


class Crypt:
    """Crypt class"""

    @staticmethod
    def hashpsw(password: str) -> str:
        """
        Hash string

        :param password: str
        :return: str
        """

        return bcrypt.hashpw(password.encode('utf8'), bcrypt.gensalt())

    @staticmethod
    def gen_password(length: int) -> str:
        """
        Generate safety password

        :param length: int
        :return: str
        """
        alphabet = string.ascii_letters + string.digits
        password = ''.join(choice(alphabet) for _ in range(length))

        return password

    @staticmethod
    def gen_random(start: int, end: int) -> int:
        """
        Generate random int

        :param start: int
        :param end: int
        :return: int
        """

        return randint(start, end)

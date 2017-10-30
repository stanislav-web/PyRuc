# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from ..exceptions import RepositoryError


class RedisRepositoryError(RepositoryError):
    """RedisRepositoryError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RedisRepositoryError.__class__.__name__
        self.message = str(message)

        super(RedisRepositoryError, self).__init__(message)

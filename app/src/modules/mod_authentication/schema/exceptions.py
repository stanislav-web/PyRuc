# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class UserSchemaError(Exception):
    """UserSchemaError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        if isinstance(message, dict):
            merged = []
            for _, value in message.items():
                merged += value
            message = merged

        self.type = UserSchemaError.__class__.__name__
        self.message = message

        super(UserSchemaError, self).__init__(message)

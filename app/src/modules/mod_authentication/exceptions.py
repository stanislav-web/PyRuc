# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class AuthenticationRequestError(Exception):
    """AuthenticationRequestError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = AuthenticationRequestError.__class__.__name__
        self.message = message

        super(AuthenticationRequestError, self).__init__(message)


class AuthenticationNotFoundError(Exception):
    """AuthenticationNotFoundError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = AuthenticationNotFoundError.__class__.__name__
        self.message = message

        super(AuthenticationNotFoundError, self).__init__(message)


class AuthenticationForbiddenError(Exception):
    """AuthenticationForbiddenError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = AuthenticationForbiddenError.__class__.__name__
        self.message = message

        super(AuthenticationForbiddenError, self).__init__(message)

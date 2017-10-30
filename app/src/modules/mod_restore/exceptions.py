# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class RestoreRequestError(Exception):
    """RestoreRequestError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RestoreRequestError.__class__.__name__
        self.message = message

        super(RestoreRequestError, self).__init__(message)


class RestoreNotFoundError(Exception):
    """RestoreNotFoundError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RestoreNotFoundError.__class__.__name__
        self.message = message

        super(RestoreNotFoundError, self).__init__(message)


class RestoreUnavailableError(Exception):
    """RestoreUnavailableError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RestoreUnavailableError.__class__.__name__
        self.message = message

        super(RestoreUnavailableError, self).__init__(message)

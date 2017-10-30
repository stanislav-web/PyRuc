# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class NotFoundError(Exception):
    """NotFoundError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = NotFoundError.__class__.__name__
        self.message = message

        super(NotFoundError, self).__init__(message)


class ForbiddenError(Exception):
    """ForbiddenError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = ForbiddenError.__class__.__name__
        self.message = message

        super(ForbiddenError, self).__init__(message)

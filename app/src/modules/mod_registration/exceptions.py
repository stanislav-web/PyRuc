# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class RegistrationRequestError(Exception):
    """RegistrationRequestError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RegistrationRequestError.__class__.__name__
        self.message = message

        super(RegistrationRequestError, self).__init__(message)


class RegistrationConflictError(Exception):
    """RegistrationConflictError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RegistrationConflictError.__class__.__name__
        self.message = message

        super(RegistrationConflictError, self).__init__(message)


class RegistrationUnavailableError(Exception):
    """RegistrationUnavailableError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = RegistrationUnavailableError.__class__.__name__
        self.message = message

        super(RegistrationUnavailableError, self).__init__(message)

# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


class SmsGatewayError(Exception):
    """SmsGatewayError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = SmsGatewayError.__class__.__name__
        self.message = message

        super(SmsGatewayError, self).__init__(message)

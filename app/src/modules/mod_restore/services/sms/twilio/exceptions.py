# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from ..exceptions import SmsGatewayError


class TwilioGatewayError(SmsGatewayError):
    """TwilioGatewayError class"""

    def __init__(self, message):
        """
        Error message
        :param message: message
        :return: None
        """

        self.type = TwilioGatewayError.__class__.__name__
        self.message = str(message)

        super(TwilioGatewayError, self).__init__(message)

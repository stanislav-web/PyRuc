# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os
from twilio.rest import Client
from twilio.base.exceptions import TwilioException
from .exceptions import TwilioGatewayError
from ..interface import SmsGatewayInterface


class TwilioGateway(SmsGatewayInterface):
    """TwilioGateway class"""

    TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID', 'ACfba6742794f57556d26f2362be925e03')
    TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN', '5591456e24738c0c45277d1326c58f20')
    TWILIO_SEND_FROM = os.getenv('TWILIO_SEND_FROM', '+15005550006')

    def __init__(self):
        """
        Init connection to Twilio
        """

        super().__init__()
        try:
            self.client = Client(self.TWILIO_ACCOUNT_SID, self.TWILIO_AUTH_TOKEN)
        except TwilioException as error:
            raise TwilioGatewayError(error)

    def send_sms(self, to: str, message: str) -> str:
        """
        Send SMS

        :param to: int
        :param message: int
        :return: str
        """

        try:

            response = self.client.messages.create(
                to=to,
                from_=self.TWILIO_SEND_FROM,
                body=message)
            return response.sid

        except TwilioException as error:
            raise TwilioGatewayError(error)

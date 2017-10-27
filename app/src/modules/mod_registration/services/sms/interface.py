# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""


import abc


class SmsGatewayInterface(metaclass=abc.ABCMeta):
    """SmsGatewayInterface class"""

    def __init__(self):
        """
        Initialize interface
        """

        super(SmsGatewayInterface, self).__init__()

    @abc.abstractmethod
    def send_sms(self, to: str, message: str) -> str:
        """
        Send SMS

        :param to: int
        :param message: int
        :return: str
        """

        pass

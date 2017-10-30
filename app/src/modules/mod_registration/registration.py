# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os

from .lib import Crypt
from .services.db import RepositoryInterface, RepositoryError
from .services.sms import SmsGatewayInterface, SmsGatewayError
from .services.response import ConflictError


class Registration(object):
    """Registration class"""

    APPLICATION_REG_CODE_TTL = int(os.getenv('APPLICATION_REG_CODE_TTL', 36000))
    APPLICATION_USERPWD_LENGTH = int(os.getenv('APPLICATION_USERPWD_LENGTH', 12))

    @staticmethod
    def create_schema(schema, credentials: dict):
        """
        Create user schema

        :param schema:
        :param credentials: dict
        :return:
        """
        return schema.load(credentials)

    @staticmethod
    def create_sms_code(repository: RepositoryInterface, phone: str) -> int:
        """
        Create sms code

        :param phone: str
        :param repository: RepositoryInterface
        :return: str
        """

        code = Crypt.gen_random(10000, 99999)
        result = repository.add_reg_code(phone, code, Registration.APPLICATION_REG_CODE_TTL)
        if True is not result:
            raise RepositoryError('Unable to create user\'s key-code')
        return code

    @staticmethod
    def send_sms_code(gateway: SmsGatewayInterface, phone: str, code: str) -> None:
        """
        Send sms code

        :param gateway: SmsGatewayInterface
        :param phone: str
        :param code: str
        :return: None
        """

        sid = gateway.send_sms(to=phone, message=code)
        if False is isinstance(sid, str):
            raise SmsGatewayError('Send sms failed. Please ask your SMS provider')

    @staticmethod
    def check_sms_code(repository: RepositoryInterface, phone: str, code: str) -> None:
        """
        Check sms code for existence
        :param repository: RepositoryInterface
        :param phone: str
        :param code: str
        :return: bool
        """

        db_code = int(repository.fetch_reg_code(phone) or 0)
        if int(code) != db_code:
            raise RepositoryError('Invalid code')

        return None

    @staticmethod
    def check_user(repository: RepositoryInterface, phone: str) -> None:
        """
        Check if user already registered

        :param repository: RepositoryInterface
        :param phone: str
        :return: bool
        """

        registered = repository.is_user_exist(phone)
        if True is registered:
            raise ConflictError('The user already registered')
        return None

    @staticmethod
    def create_user(user_model, schema, repository: RepositoryInterface, phone: str) -> dict:
        """
        Create user from model

        :param user_model:
        :param schema:
        :param repository: RepositoryInterface
        :param phone: str
        :return: dict
        """

        password = Crypt.gen_password(Registration.APPLICATION_USERPWD_LENGTH)
        password_hash = Crypt.hashpsw(password)
        user = user_model(phone, password_hash)
        user_schema, _ = schema.dump(user)
        user_id = repository.create_user(user_schema)

        return {
            'user_id': user_id,
            'phone': user_schema.get('phone'),
            'password': password,
        }

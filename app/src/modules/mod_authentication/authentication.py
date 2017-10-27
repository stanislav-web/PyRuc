# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from .lib import Crypt
from .services.db import RepositoryInterface
from .services.response import NotFoundError, ForbiddenError


class Authentication(object):
    """Authentication class"""

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
    def auth(user_model, schema, repository: RepositoryInterface, phone: str, password: str) -> dict:
        """
        Auth user from model

        :param user_model:
        :param schema:
        :param repository: RepositoryInterface
        :param phone: str
        :param password: str
        :return: dict
        """

        user = user_model(phone, password)
        user_schema, _ = schema.dump(user)

        db_user = repository.get_user(user_schema.get('phone'))

        if False is bool(db_user):
            raise NotFoundError('User not found')

        valid = Crypt.checkpsw(user_schema.get('password'), db_user.get('password_hash'))

        if False is valid:
            raise ForbiddenError('Invalid credentials')

        encode = Crypt.jwt_encode({
            'user_id': db_user.get('user_id'),
            'phone': user_schema.get('phone')
        })

        return encode

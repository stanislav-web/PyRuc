# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os
import jwt
import bcrypt
from datetime import datetime, timedelta


class Crypt:
    """Crypt class"""

    JWT_TOKEN_EXP_DELTA_SECONDS = int(os.getenv('JWT_TOKEN_EXP_DELTA_SECONDS', 60))
    JWT_TOKEN_SECRET = os.getenv('JWT_TOKEN_SECRET', 'secret')
    JWT_TOKEN_ALGORITHM = os.getenv('JWT_TOKEN_ALGORITHM', 'HS256')

    @staticmethod
    def jwt_encode(payload: dict) -> dict:
        """
        Encode data into jwt

        :param payload: dict
        :return: dict
        """

        payload['exp'] = datetime.utcnow() + timedelta(seconds=Crypt.JWT_TOKEN_EXP_DELTA_SECONDS)
        encoded = jwt.encode(payload, Crypt.JWT_TOKEN_SECRET, algorithm=Crypt.JWT_TOKEN_ALGORITHM)

        return {
            'token': encoded.decode('utf8'),
            'expires': payload['exp']
        }

    @staticmethod
    def jwt_decode(token: str) -> dict:
        """
        Decode data from jwt

        :param token: str
        :return: dict
        """

        decoded = jwt.decode(token, Crypt.JWT_TOKEN_SECRET, algorithms=[Crypt.JWT_TOKEN_ALGORITHM])
        return decoded

    @staticmethod
    def checkpsw(password: str, hashed_password: str) -> bool:
        """
        Check input password

        :param password: str
        :param hashed_password: str
        :return: str
        """

        return bcrypt.checkpw(password.encode('utf8'), hashed_password.encode('utf8'))

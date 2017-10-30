# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from .authentication import Authentication
from .schema import User, UserSchema, UserSchemaError
from .services.response import NotFoundError, ForbiddenError
from .services.db import RepositoryError
from .services.db.redis import RedisRepository
from .exceptions import AuthenticationNotAvailableError, AuthenticationRequestError, \
    AuthenticationNotFoundError, AuthenticationForbiddenError


def login(credentials: dict) -> dict:
    """
    User login

    :param credentials: dict
    :return: dict
    """

    try:
        result, errors = Authentication.create_schema(UserSchema(), credentials)

        if 0 < len(errors):
            raise UserSchemaError(errors)

        token = Authentication.auth(User, UserSchema(), RedisRepository(), result.get('phone'), result.get('password'))
        return token
    except UserSchemaError as error:
        raise AuthenticationRequestError(error.message)
    except RepositoryError as error:
        raise AuthenticationNotAvailableError(error.message)
    except NotFoundError as error:
        raise AuthenticationNotFoundError(error.message)
    except ForbiddenError as error:
        raise AuthenticationForbiddenError(error.message)

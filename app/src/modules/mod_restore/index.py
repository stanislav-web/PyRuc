# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from .restore import Restore
from .schema import User, UserSchemaDump, UserSchemaStepOne, UserSchemaStepTwo, UserSchemaError
from .services.db import RepositoryError
from .services.sms import SmsGatewayError
from .services.response import NotFoundError
from .services.db.redis import RedisRepository
from .services.sms.twilio import TwilioGateway
from .exceptions import RestoreRequestError, RestoreUnavailableError, RestoreNotFoundError


def step_one(credentials: dict) -> dict:
    """
    Restore Step 1

    :param credentials: dict
    :return: dict
    """

    try:
        result, errors = Restore.create_schema(UserSchemaStepOne(), credentials)

        if 0 < len(errors):
            raise UserSchemaError(errors)

        Restore.check_user(RedisRepository(), result.get('phone'))

        sms_code = Restore.create_sms_code(RedisRepository(), result.get('phone'))

        Restore.send_sms_code(TwilioGateway(), result.get('phone'), str(sms_code))

        return {'code': sms_code}

    except UserSchemaError as error:
        raise RestoreRequestError(error.message)
    except NotFoundError as error:
        raise RestoreNotFoundError(error.message)
    except (SmsGatewayError, RepositoryError) as error:
        raise RestoreUnavailableError(error.message)


def step_two(credentials: dict) -> dict:
    """
    Restore Step 2

    :param credentials: dict
    :return: dict
    """

    try:
        result, errors = Restore.create_schema(UserSchemaStepTwo(), credentials)

        if 0 < len(errors):
            raise UserSchemaError(errors)

        Restore.check_sms_code(RedisRepository(), result.get('phone'), result.get('code'))
        user_id = Restore.get_user_id(RedisRepository(), result.get('phone'))
        user = Restore.update_user_password(User, UserSchemaDump(), RedisRepository(), user_id, result.get('phone'))
        return user

    except UserSchemaError as error:
        raise RestoreRequestError(error.message)
    except (SmsGatewayError, RepositoryError) as error:
        raise RestoreUnavailableError(error.message)

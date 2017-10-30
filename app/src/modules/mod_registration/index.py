# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from .registration import Registration
from .schema import User, UserSchemaDump, UserSchemaStepOne, UserSchemaStepTwo, UserSchemaError
from .services.db import RepositoryError
from .services.sms import SmsGatewayError
from .services.response import ConflictError
from .services.db.redis import RedisRepository
from .services.sms.twilio import TwilioGateway
from .exceptions import RegistrationRequestError, RegistrationUnavailableError, RegistrationConflictError


def step_one(credentials: dict) -> dict:
    """
    Registration Step 1

    :param credentials: dict
    :return: dict
    """

    try:
        result, errors = Registration.create_schema(UserSchemaStepOne(), credentials)

        if 0 < len(errors):
            raise UserSchemaError(errors)

        Registration.check_user(RedisRepository(), result.get('phone'))

        sms_code = Registration.create_sms_code(RedisRepository(), result.get('phone'))

        Registration.send_sms_code(TwilioGateway(), result.get('phone'), str(sms_code))

        return {'code': sms_code}

    except UserSchemaError as error:
        raise RegistrationRequestError(error.message)
    except ConflictError as error:
        raise RegistrationConflictError(error.message)
    except (SmsGatewayError, RepositoryError) as error:
        raise RegistrationUnavailableError(error.message)


def step_two(credentials: dict) -> dict:
    """
    Registration Step 2

    :param credentials: dict
    :return: dict
    """

    try:
        result, errors = Registration.create_schema(UserSchemaStepTwo(), credentials)

        if 0 < len(errors):
            raise UserSchemaError(errors)

        Registration.check_sms_code(RedisRepository(), result.get('phone'), result.get('code'))
        user = Registration.create_user(User, UserSchemaDump(), RedisRepository(), result.get('phone'))
        return user

    except UserSchemaError as error:
        raise RegistrationRequestError(error.message)
    except (SmsGatewayError, RepositoryError) as error:
        raise RegistrationUnavailableError(error.message)

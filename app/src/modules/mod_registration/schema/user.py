# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from marshmallow import Schema, fields, validate, ValidationError


class UserSchemaDump(Schema):
    """UserSchemaDump class"""

    phone = fields.Integer()
    password_hash = fields.String()
    create_date = fields.Integer()
    is_active = fields.Boolean()


class UserSchemaStepOne(Schema):
    """UserSchemaStepOne class"""

    MIN, MAX = (5, 12)

    @staticmethod
    def must_be_valid_phone(data):
        """
        Check if data is phone number

        :param data: str
        :return: None
        """

        if False is data.isdigit():
            raise ValidationError('Please provide a valid phone number.')

    phone = fields.String(
        required=True,
        validate=[must_be_valid_phone.__get__(object, type(object)),
                  validate.Length(min=MIN, max=MAX,
                                  error='Length must be between {:d} and {:d}'.format(MIN, MAX)
                                  )],
        error_messages={
            'required': 'Phone is required.'
        }
    )


class UserSchemaStepTwo(UserSchemaStepOne):
    """UserSchemaStepTwo class"""

    EQUAL = 5

    @staticmethod
    def must_be_valid_code(data):
        """
        Check if data is code

        :param data: str
        :return: None
        """

        if False is data.isdigit():
            raise ValidationError('Please provide a valid code.')

    code = fields.String(
        required=True,
        validate=[must_be_valid_code.__get__(object, type(object)),
                  validate.Length(equal=EQUAL,
                                  error='Code must be equal {:d} chars'.format(EQUAL)
                                  )],
        error_messages={
            'required': 'Code is required.'
        }
    )

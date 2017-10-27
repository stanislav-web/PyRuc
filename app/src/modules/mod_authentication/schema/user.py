# -*- coding: utf-8 -*-

""" EXCHANGE-ACCESS-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

from marshmallow import Schema, fields, validate, ValidationError


class UserSchema(Schema):
    """UserSchema class"""

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
    password = fields.String(
        required=True,
        error_messages={
            'required': 'Password is required.'
        }
    )

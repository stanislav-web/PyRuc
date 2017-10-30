# -*- coding: utf-8 -*-

""" PyRuc-UAC-SERVICE
    Copyright (C) 2007 Free Software Foundation, Inc.
    Everyone is permitted to copy and distribute verbatim copies of this license document,
    but changing it is not allowed.
    Development Team: Stanislav WEB
"""

import os
import unittest2 as unittest
import json
import sys

from http import HTTPStatus
from src import application
from src.modules.mod_authentication.services.db.redis import RedisRepository


class DevNull(object):
    def write(self, data):
        pass

class ModAuthenticationTestCase(unittest.TestCase):
    """ ModAuthenticationTestCase class """

    def registration(self):
        res1 = self.app.post('/registration/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))
        rdict = json.loads(res1.data.decode())
        message = rdict.get('message')

        res2 = self.app.post('/registration/s2', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            code=message.get('code')
        ))
        rdict = json.loads(res2.data.decode())
        message = rdict.get('message')
        self.password = message.get('password')


    @classmethod
    def setUpClass(cls):
        """
        Flush redis
        """

        super(ModAuthenticationTestCase, cls).setUpClass()
        RedisRepository().get_instance().flushdb()

    def setUp(self):
        application.testing = True
        self.app = application.test_client()
        self.old_stderr = sys.stderr
        sys.stderr = DevNull()

    def test_0_authentication_ok(self):

        self.registration()

        res = self.app.post('/authentication', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            password=self.password
        ))

        self.assertEqual(HTTPStatus.OK, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        message = rdict.get('message')
        self.assertTrue(isinstance(rdict.get('message'), dict))
        self.assertTrue('expires' in message)
        self.assertTrue('token' in message)

    def test_1_authentication_request_error(self):

        res = self.app.post('/authentication', data=dict(
            phone='34kfk43466234',
            password='invalid'
        ))

        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), list))

    def test_2_authentication_request_forbidden(self):

        res = self.app.post('/authentication', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            password='invalid'
        ))

        self.assertEqual(HTTPStatus.FORBIDDEN, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), str))

    def test_3_authentication_user_not_found(self):

        res = self.app.post('/authentication', data=dict(
            phone=34499340058,
            password='invalid'
        ))

        self.assertEqual(HTTPStatus.NOT_FOUND, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), str))

    def tearDown(self):
        sys.stderr = self.old_stderr

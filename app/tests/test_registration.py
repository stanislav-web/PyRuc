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
from src.modules.mod_registration.services.db.redis import RedisRepository


class DevNull(object):
    def write(self, data):
        pass

class ModRegistrationTestCase(unittest.TestCase):
    """ ModRegistrationTestCase class """

    @classmethod
    def setUpClass(cls):
        """
        Flush redis
        """

        super(ModRegistrationTestCase, cls).setUpClass()
        RedisRepository().get_instance().flushdb()

    def setUp(self):
        application.testing = True
        self.app = application.test_client()
        self.old_stderr = sys.stderr
        sys.stderr = DevNull()

    def test_0_registration_s1_created(self):
        res = self.app.post('/registration/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))

        self.assertEqual(HTTPStatus.CREATED, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), dict))

    def test_1_registration_s1_request_error(self):

        res = self.app.post('/registration/s1', data=dict(
            phone='34kfk43466234'
        ))

        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), list))

    def test_2_registration_s2(self):

        res1 = self.app.post('/registration/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res1.content_type)
        self.assertTrue(isinstance(res1.data, bytes))

        rdict = json.loads(res1.data.decode())
        message = rdict.get('message')
        res2 = self.app.post('/registration/s2', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            code=message.get('code')
        ))
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res1.content_type)
        self.assertTrue(isinstance(res1.data, bytes))
        self.assertEqual(HTTPStatus.CREATED, res2.status_code)
        rdict = json.loads(res2.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), dict))
        message = rdict.get('message')
        self.assertTrue('password' in message)
        self.assertTrue('phone' in message)
        self.assertTrue('user_id' in message)

    def test_3_registration_s1_conflict_request_error(self):

        res = self.app.post('/registration/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))

        self.assertEqual(HTTPStatus.CONFLICT, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), str))

    def test_3_registration_s2_request_error(self):

        res = self.app.post('/registration/s1', data=dict(
            phone='34kfk43466234',
            code='invalid'
        ))

        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), list))

    def tearDown(self):
        sys.stderr = self.old_stderr

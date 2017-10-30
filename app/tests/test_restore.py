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
from dotenv import load_dotenv
from src import application
from src.modules.mod_restore.services.db.redis import RedisRepository


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path, verbose=True)


class DevNull(object):
    def write(self, data):
        pass

class ModRestoreTestCase(unittest.TestCase):
    """ ModRestoreTestCase class """

    def registration(self):
        res1 = self.app.post('/registration/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))
        rdict = json.loads(res1.data.decode())
        message = rdict.get('message')
        self.app.post('/registration/s2', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            code=message.get('code')
        ))

    @classmethod
    def setUpClass(cls):
        """
        Flush redis
        """

        super(ModRestoreTestCase, cls).setUpClass()
        RedisRepository().get_instance().flushdb()

    def setUp(self):
        application.testing = True
        self.app = application.test_client()
        self.old_stderr = sys.stderr
        sys.stderr = DevNull()

    def test_0_restore_s1_created(self):

        self.registration()

        res = self.app.post('/restore/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))

        self.assertEqual(HTTPStatus.CREATED, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), dict))

    def test_1_restore_s1_request_error(self):
        res = self.app.post('/restore/s1', data=dict(
            phone='34kfk43466234'
        ))

        self.assertEqual(HTTPStatus.BAD_REQUEST, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), list))

    def test_2_restore_s1_user_not_found(self):

        res = self.app.post('/restore/s1', data=dict(
            phone='347823402474'
        ))

        self.assertEqual(HTTPStatus.NOT_FOUND, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), str))

    def test_3_restore_s2(self):

        RedisRepository().get_instance().flushdb()
        self.registration()

        res1 = self.app.post('/restore/s1', data=dict(
            phone=os.getenv('TEST_PHONE_NO')
        ))
        rdict = json.loads(res1.data.decode())
        message = rdict.get('message')
        res2 = self.app.post('/restore/s2', data=dict(
            phone=os.getenv('TEST_PHONE_NO'),
            code=message.get('code')
        ))

        self.assertEqual(HTTPStatus.CREATED, res2.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res2.content_type)
        self.assertTrue(isinstance(res2.data, bytes))

        rdict = json.loads(res2.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), dict))
        message = rdict.get('message')
        self.assertTrue('password' in message)
        self.assertTrue('phone' in message)
        self.assertTrue('user_id' in message)

    def test_4_restore_s2_request_error(self):

        res = self.app.post('/restore/s2', data=dict(
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

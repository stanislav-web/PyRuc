# -*- coding: utf-8 -*-

""" PyRuc-Python Redis Users Controller
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
from src.modules.mod_registration.services.db.redis import RedisRepository

dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
load_dotenv(dotenv_path, verbose=True)


class DevNull(object):
    def write(self, data):
        pass


class InvalidResponsesTestCase(unittest.TestCase):
    """ InvalidResponsesTestCase class """

    @classmethod
    def setUpClass(cls):
        """
        Flush redis
        """

        super(InvalidResponsesTestCase, cls).setUpClass()
        RedisRepository().get_instance().flushdb()

    def setUp(self):
        application.testing = True
        self.app = application.test_client()
        self.old_stderr = sys.stderr
        sys.stderr = DevNull()

    def test_0_service_unavailable(self):
        res = self.app.post('/registration/s1', data=dict(
            phone=25005550006 # invalid phone : no sms 503
        ))

        self.assertEqual(HTTPStatus.SERVICE_UNAVAILABLE, res.status_code)
        self.assertEqual(os.getenv('TEST_EXPECTED_CTYPE'), res.content_type)
        self.assertTrue(isinstance(res.data, bytes))
        rdict = json.loads(res.data.decode())
        self.assertTrue(isinstance(rdict.get('message'), str))

    def tearDown(self):
        sys.stderr = self.old_stderr

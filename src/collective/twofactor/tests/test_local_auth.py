# -*- coding: utf-8 -*-

import unittest2 as unittest

from datetime import datetime
from hashlib import sha256

from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getMultiAdapter


class TestLocalAuth(unittest.TestCase):

    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.member = self.pm_tool.getAuthenticatedMember()
        self.local_auth = getMultiAdapter((self.member, self.request),
                                          ILocalAuthenticationMethod,
                                          'test')

    def test_generate_session_hash(self):
        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')

        self.local_auth.generate_session_hash()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')

        self.assertNotEqual(two_factor_hash, '')
        self.assertNotEqual(two_factor_hash_date, '')

        h = sha256("%s%s" % (self.member.id, two_factor_hash_date)).hexdigest()

        self.assertEqual(two_factor_hash, h)

    def test_valid_session_hash(self):
        self.assertFalse(self.local_auth.is_valid_session())
        self.local_auth.generate_session_hash()
        # If we check if this session is valid, we are getting false, because
        # it should be in a cookie
        self.assertFalse(self.local_auth.is_valid_session())

        # So let's create the cookie
        cookie_name = 'collective.twofactor.two_factor_hash'
        hash_value = self.request.response.cookies[cookie_name]['value']
        self.request.cookies[cookie_name] = hash_value

        # And now, we should get True
        self.assertTrue(self.local_auth.is_valid_session())

        # Override hash generation date
        hash_date = datetime(2001, 1, 1).strftime("%Y-%m-%dT%H:%M:%S")
        self.member.setProperties({'two_factor_hash_date': hash_date})
        self.assertFalse(self.local_auth.is_valid_session())

    def test_generate_random_code(self):
        # Assign some stuff to member properties
        self.member.setProperties({'two_factor_hash': '12345',
                                   'two_factor_hash_date': '67890',
                                   'local_code': 'a',
                                   'local_code_date': 'b',
                                   'local_code_sent': True,
                                   })

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '12345')
        self.assertEqual(two_factor_hash_date, '67890')
        self.assertEqual(local_code, 'a')
        self.assertEqual(local_code_date, 'b')
        self.assertTrue(local_code_sent)

        self.local_auth.generate_random_code()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertNotEqual(local_code, 'a')
        self.assertNotEqual(local_code_date, 'b')
        self.assertFalse(local_code_sent)

        # Do a statistically long test to be sure we get proper length codes
        lengths = [10, 14, 20]
        for length in lengths:
            for i in range(1000):
                self.local_auth.generate_random_code(length=length)
                self.assertEqual(len(self.local_auth.get_code()), length)

    def test_valid_code(self):
        local_code = self.local_auth.get_code()
        self.assertFalse(self.local_auth.valid_code(local_code))

        self.local_auth.generate_random_code()

        local_code = self.local_auth.get_code()
        self.assertTrue(self.local_auth.valid_code(local_code))

        # Override local_code_date to make it fail
        local_code_date = datetime(2001, 1, 1).strftime("%Y-%m-%dT%H:%M:%S")
        self.member.setProperties({'local_code_date': local_code_date})

        self.assertFalse(self.local_auth.valid_code(local_code))

    def test_reset_code(self):
        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)

        self.assertEqual(self.local_auth.status, {})

        self.local_auth.reset_code()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertNotEqual(local_code, '')
        self.assertNotEqual(local_code_date, '')
        self.assertTrue(local_code_sent)

        self.assertEqual(self.local_auth.status['status'], u'success')
        self.assertEqual(self.local_auth.status['message'],
                         self.local_auth.new_code_sent)

        # Make it fail
        self.local_auth.should_fail_sending = True
        self.local_auth.reset_code()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)

        self.assertEqual(self.local_auth.status['status'], u'error')
        self.assertEqual(self.local_auth.status['message'],
                         self.local_auth.error_sending)

    def test_execute(self):
        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)

        self.assertEqual(self.local_auth.status, {})

        self.local_auth.execute()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertNotEqual(local_code, '')
        self.assertNotEqual(local_code_date, '')
        self.assertTrue(local_code_sent)

        self.assertEqual(self.local_auth.status['status'], u'success')
        self.assertEqual(self.local_auth.status['message'],
                         self.local_auth.new_code_sent)

        # If execute again, code was already sent
        self.local_auth.execute()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertNotEqual(local_code, '')
        self.assertNotEqual(local_code_date, '')
        self.assertTrue(local_code_sent)

        self.assertEqual(self.local_auth.status['status'], u'success')
        self.assertEqual(self.local_auth.status['message'],
                         self.local_auth.valid_already_sent)

        # Override the sent date and make it fail
        local_code_date = datetime(2001, 1, 1).strftime("%Y-%m-%dT%H:%M:%S")
        self.member.setProperties({'local_code_date': local_code_date})
        self.local_auth.should_fail_sending = True
        self.local_auth.execute()

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        local_code = self.local_auth.get_code()

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)

        self.assertEqual(self.local_auth.status['status'], u'error')
        self.assertEqual(self.local_auth.status['message'],
                         self.local_auth.error_sending)

# -*- coding: utf-8 -*-

import unittest2 as unittest

from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getAdapter


class TestEmailMethod(unittest.TestCase):

    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.member = self.pm_tool.getAuthenticatedMember()
        self.local_auth = getAdapter(self.member,
                                     ILocalAuthenticationMethod,
                                     'email')

    def test_email_failed(self):
        self.member.setProperties({'email': 'should@fail.com'})
        self.assertFalse(self.local_auth.failure)
        self.local_auth.generate_random_code()
        self.local_auth.send_code()
        self.assertTrue(self.local_auth.failure)

    def test_email_success(self):
        self.member.setProperties({'email': 'should@succeed.com'})
        self.assertFalse(self.local_auth.failure)
        self.local_auth.generate_random_code()
        self.local_auth.send_code()
        self.assertFalse(self.local_auth.failure)

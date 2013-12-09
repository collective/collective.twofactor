# -*- coding: utf-8 -*-

import unittest2 as unittest

from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getAdapter


class TestSMSMethod(unittest.TestCase):

    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.member = self.pm_tool.getAuthenticatedMember()
        self.local_auth = getAdapter(self.member,
                                     ILocalAuthenticationMethod,
                                     'sms')

    def test_sms_failed(self):
        self.member.setProperties({'cell_phone': '0'})
        self.assertFalse(self.local_auth.failure)
        self.local_auth.generate_random_code()
        self.local_auth.send_code()
        self.assertTrue(self.local_auth.failure)

    def test_sms_success(self):
        self.member.setProperties({'cell_phone': '1'})
        self.assertFalse(self.local_auth.failure)
        self.local_auth.generate_random_code()
        self.local_auth.send_code()
        self.assertFalse(self.local_auth.failure)

# -*- coding: utf-8 -*-

import unittest2 as unittest

#from Testing.makerequest import makerequest

from collective.twofactor.interfaces import ITwoFactorLayer
from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getAdapter
from zope.event import notify
from zope.interface import alsoProvides
from ZPublisher.pubevents import PubSuccess


class TestRedirectEvent(unittest.TestCase):
    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, ITwoFactorLayer)
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.member = self.pm_tool.getAuthenticatedMember()
        self.local_auth = getAdapter(self.member,
                                     ILocalAuthenticationMethod,
                                     'test')

    def test_do_not_redirect_if_no_method_chosen(self):
        self.member.setProperties({'two_factor_method': ''})
        self.request.set("PATH_INFO", "http://nohost/plone")
        notify(PubSuccess(self.request))
        self.assertEqual(self.request.response.getStatus(), 200)

    def test_redirect_if_method_chosen(self):
        self.member.setProperties({'two_factor_method': 'test'})
        self.request.set("PATH_INFO", "http://nohost/plone")
        notify(PubSuccess(self.request))
        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         ("http://nohost/plone/two-factor-challenge?came_from="
                          "http://nohost"))

    def test_ignored_path(self):
        self.member.setProperties({'two_factor_method': 'test'})
        self.request.set("PATH_INFO", "http://nohost/two-factor-challenge")
        notify(PubSuccess(self.request))
        self.assertEqual(self.request.response.getStatus(), 200)

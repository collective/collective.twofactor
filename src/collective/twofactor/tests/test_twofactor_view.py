# -*- coding: utf-8 -*-

import unittest2 as unittest

#from Testing.makerequest import makerequest

from collective.twofactor.interfaces import ITwoFactorLayer
from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getAdapter
from zope.component import getMultiAdapter
from zope.interface import alsoProvides


class TestTwoFactorView(unittest.TestCase):
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

    def test_do_not_render_if_no_method_chosen(self):
        self.member.setProperties({'two_factor_method': ''})
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        self.assertIsNone(view())

    def test_render_if_method_chosen(self):
        self.member.setProperties({'two_factor_method': 'test'})
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()
        self.assertIn("Two-factor Authentication", rendered)
        self.assertIn("New code has been sent.", rendered)
        self.assertNotIn("Valid code already sent.", rendered)

        # If called again
        rendered = view()
        self.assertIn("Two-factor Authentication", rendered)
        self.assertNotIn("New code has been sent.", rendered)
        self.assertIn("Valid code already sent.", rendered)

        # If asked to reset password
        self.request.set("reset_code", "1")
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()
        self.assertIn("Two-factor Authentication", rendered)
        self.assertIn("New code has been sent.", rendered)
        self.assertNotIn("Valid code already sent.", rendered)

    def test_error_if_invalid_code(self):
        self.member.setProperties({'two_factor_method': 'test'})
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.request.set("two-factor-token", "1234567")
        self.request.set("submit", "1")
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.assertIn("Two-factor Authentication", rendered)
        self.assertIn("The code you entered is invalid, please try again",
                      rendered)
        self.assertNotIn("New code has been sent.", rendered)
        self.assertNotIn("Valid code already sent.", rendered)

    def test_redirect_to_context_if_not_came_from(self):
        self.member.setProperties({'two_factor_method': 'test'})
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.request.set("two-factor-token", "12345678")
        self.request.set("submit", "1")
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.assertIn("Two-factor Authentication", rendered)
        self.assertNotIn("The code you entered is invalid, please try again",
                         rendered)

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         'http://nohost/plone')

    def test_redirect_to_came_from(self):
        self.member.setProperties({'two_factor_method': 'test'})
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.request.set("two-factor-token", "12345678")
        self.request.set("submit", "1")
        self.request.set("came_from", "http://nohost/custom/path")
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.assertIn("Two-factor Authentication", rendered)
        self.assertNotIn("The code you entered is invalid, please try again",
                         rendered)

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         'http://nohost/custom/path')

        self.request.set("two-factor-token", "12345678")
        self.request.set("submit", "1")
        self.request.set("came_from", "http://nohost/login_form")
        view = getMultiAdapter((self.portal, self.request),
                               name="two-factor-challenge")
        rendered = view()

        self.assertIn("Two-factor Authentication", rendered)
        self.assertNotIn("The code you entered is invalid, please try again",
                         rendered)

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         'http://nohost/logged_in')

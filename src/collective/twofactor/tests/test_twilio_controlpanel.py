# -*- coding: utf-8 -*-

import unittest2 as unittest

from collective.twofactor.controlpanel import ITwilioSettings
from collective.twofactor.interfaces import ITwoFactorLayer
from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from plone.registry.interfaces import IRegistry

from Products.CMFCore.utils import getToolByName

from zope.component import getMultiAdapter
from zope.component import getUtility
from zope.interface import alsoProvides


class TestTwilioControlpanel(unittest.TestCase):
    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.request = self.layer['request']
        alsoProvides(self.request, ITwoFactorLayer)
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.member = self.pm_tool.getAuthenticatedMember()
        registry = getUtility(IRegistry)
        self.settings = registry.forInterface(ITwilioSettings)

    def test_invalid_values(self):
        self.request.set("form.widgets.account_sid", u"valid_sid")
        self.request.set("form.widgets.auth_token", u"invalid_token")
        self.request.set("form.widgets.phone_number", u"invalid_phone")
        self.request.set("form.buttons.save", u"Submit")

        view = getMultiAdapter((self.portal, self.request),
                               name="twilio-settings")
        rendered = view()

        self.assertIn("The SID or token are invalid", rendered)
        self.assertEqual(self.settings.account_sid, None)
        self.assertEqual(self.settings.auth_token, None)
        self.assertEqual(self.settings.phone_number, None)

        self.request.set("form.widgets.account_sid", u"valid_sid")
        self.request.set("form.widgets.auth_token", u"valid_token")
        self.request.set("form.widgets.phone_number", u"invalid_phone")
        self.request.set("form.buttons.save", u"Submit")

        view = getMultiAdapter((self.portal, self.request),
                               name="twilio-settings")
        rendered = view()

        self.assertIn("The phone number you entered doesn't seem valid",
                      rendered)

        self.assertEqual(self.settings.account_sid, None)
        self.assertEqual(self.settings.auth_token, None)
        self.assertEqual(self.settings.phone_number, None)

        self.request.set("form.widgets.account_sid", u"valid_sid")
        self.request.set("form.widgets.auth_token", u"valid_token")
        self.request.set("form.widgets.phone_number", u"no_sms_phone")
        self.request.set("form.buttons.save", u"Submit")

        view = getMultiAdapter((self.portal, self.request),
                               name="twilio-settings")
        rendered = view()

        self.assertIn("this phone number cannot send SMS.",
                      rendered)

        self.assertEqual(self.settings.account_sid, None)
        self.assertEqual(self.settings.auth_token, None)
        self.assertEqual(self.settings.phone_number, None)

    def test_valid_credentials(self):
        self.request.set("form.widgets.account_sid", u"valid_sid")
        self.request.set("form.widgets.auth_token", u"valid_token")
        self.request.set("form.widgets.phone_number", u"valid_phone")
        self.request.set("form.buttons.save", u"Submit")

        view = getMultiAdapter((self.portal, self.request),
                               name="twilio-settings")
        view()

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         "http://nohost/plone/plone_control_panel")

        self.assertEqual(self.settings.account_sid, u"valid_sid")
        self.assertEqual(self.settings.auth_token, u"valid_token")
        self.assertEqual(self.settings.phone_number, u"valid_phone")

    def test_cancel(self):
        self.request.set("form.widgets.account_sid", u"valid_sid")
        self.request.set("form.widgets.auth_token", u"valid_token")
        self.request.set("form.widgets.phone_number", u"valid_phone")
        self.request.set("form.buttons.cancel", u"Cancel")

        view = getMultiAdapter((self.portal, self.request),
                               name="twilio-settings")
        view()

        self.assertEqual(self.request.response.getStatus(), 302)
        self.assertEqual(self.request.response.headers['location'],
                         "http://nohost/plone/plone_control_panel")

        self.assertEqual(self.settings.account_sid, None)
        self.assertEqual(self.settings.auth_token, None)
        self.assertEqual(self.settings.phone_number, None)

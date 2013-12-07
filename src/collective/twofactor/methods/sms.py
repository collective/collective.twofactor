# -*- coding: utf-8 -*-

from base import LocalAuthentication
from collective.twofactor import _
from collective.twofactor.controlpanel import ITwilioSettings
from plone.registry.interfaces import IRegistry
from zope.browserpage import ViewPageTemplateFile
from zope.component import getUtility
from twilio.rest import TwilioRestClient


class SMSAuthentication(LocalAuthentication):

    name = _("Authentication over SMS")

    valid_already_sent = _(u"A code has already been sent to your phone.")
    new_code_sent = _(u"A new code has been generated and sent to your phone.")

    def send_code(self):
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITwilioSettings)

        client = TwilioRestClient(settings.account_sid, settings.auth_token)

        user_phone = self.member.getProperty('cell_phone', None)
        message = _("Use this code to authenticate: %s" % self.get_code())

        client.sms.messages.create(to=user_phone,
                                   from_=settings.phone_number,
                                   body=message)
        super(SMSAuthentication, self).send_code()

# -*- coding: utf-8 -*-
import sys

from base import LocalAuthentication
from collective.twofactor import _
from collective.twofactor.controlpanel import ITwilioSettings
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from zope.component.hooks import getSite
from twilio.rest import TwilioRestClient


class SMSAuthentication(LocalAuthentication):

    name = _("Authentication over SMS")

    valid_already_sent = _(u"A code has already been sent to your phone.")
    new_code_sent = _(u"A new code has been generated and sent to your phone.")
    error_sending = _(u"An error has occured while trying to send an SMS to "
                      "your phone. Please contact the site administrator for "
                      "assistance. Sorry for the inconvenience.")

    def send_code(self):
        self.failure = False
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITwilioSettings)

        client = TwilioRestClient(settings.account_sid, settings.auth_token)

        user_phone = self.member.getProperty('cell_phone', None)
        message = _("Use this code to authenticate: %s" % self.get_code())

        try:
            client.sms.messages.create(to=user_phone,
                                       from_=settings.phone_number,
                                       body=message)
        except:
            # Log in the error_log
            site = getSite()
            site.error_log.raising(sys.exc_info())
            self.failure = True

        if not self.failure:
            super(SMSAuthentication, self).send_code()

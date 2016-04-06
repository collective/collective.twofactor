# -*- coding: utf-8 -*-
import sys

from base import LocalAuthentication
from collective.twofactor import _
from plone import api
from zope.component.hooks import getSite
from zope.i18n import translate


class EmailAuthentication(LocalAuthentication):

    name = _("Authentication over Email")

    valid_already_sent = _(u"A code has already been sent to your email "
                           "address.")
    new_code_sent = _(u"A new code has been generated and sent to your email "
                      "address.")
    error_sending = _(u"An error has occured while trying to send you an "
                      "Email. Please contact the site administrator for "
                      "assistance. Sorry for the inconvenience.")

    def send_code(self):
        self.failure = False
        site_name = api.portal.get().title

        subject = translate(_(
            u"Authentication code for ${site_name}",
            mapping={'site_name': site_name}
        ), context=self.request)
        message = translate(_(
            u"Use this code to authenticate: ${code}",
            mapping={'code': self.get_code()}
        ), context=self.request)

        user_email = self.member.getProperty('email', None)
        try:
            api.portal.send_email(recipient=user_email,
                                  subject=subject,
                                  body=message)
        except:
            # Log in the error_log
            site = getSite()
            site.error_log.raising(sys.exc_info())
            self.failure = True

        if not self.failure:
            super(EmailAuthentication, self).send_code()

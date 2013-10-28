# -*- coding: utf-8 -*-

from base import LocalAuthentication
from collective.twofactor import _
from plone import api


class EmailAuthentication(LocalAuthentication):

    name = _("Authentication over Email")

    valid_already_sent = _(u"A code has already been sent to your email address.")
    new_code_sent = _(u"A new code has been generated and sent to your email address.")

    def send_code(self):
        site_name = api.portal.get().title

        subject = _(u"Authentication code for %s" % site_name)
        message = _("Use this code to authenticate: %s" % self.get_code())

        user_email = self.member.getProperty('email', None)
        api.portal.send_email(recipient=user_email,
                              subject=subject,
                              body=message)
        super(EmailAuthentication, self).send_code()

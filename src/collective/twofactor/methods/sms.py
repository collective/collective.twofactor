# -*- coding: utf-8 -*-

from base import LocalAuthentication
from collective.twofactor import _
from zope.browserpage import ViewPageTemplateFile


class SMSAuthentication(LocalAuthentication):
    
    name = _("Authentication over SMS")
    
    valid_already_sent = _(u"A code has already been sent to your phone.")
    new_code_sent = _(u"A new code has been generated and sent to your phone.")

    def send_code(self):
        import pdb;pdb.set_trace()
        super(SMSAuthentication, self).send_code()

# -*- coding: utf-8 -*-

from collective.twofactor import _
from zope.interface import Interface
from zope import schema


class ITwilioSettings(Interface):
    """ Interface for the control panel form.
    """

    account_sid = schema.TextLine(
        title=_(u"Account SID"),
        description=_(u"Your Twilio Account SID."),
        required=True,
    )

    auth_token = schema.Password(
        title=_(u"Auth Token"),
        description=_(u"Your Twilio Auth Token."),
        required=True,
    )

    phone_number = schema.TextLine(
        title=_(u"Phone Number"),
        description=_(u"Your Twilio phone number from where to send SMS. "
                       "International format, with no special characters. "
                       "Example: +15555555555"),
        required=True,
    )


class ITwoFactorLayer(Interface):
    """ A layer specific for this add-on product.
    """

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


class ITwoFactorSettings(Interface):
    """ Interface for the control panel form.
    """

    to_ignore = schema.List(
        title=_(u"Ignore these URLs"),
        description=_(u"Add here urls you don't want to check for two-factor "
                      u"auth. Useful for resources, or special pages, like "
                      u"login and two-factor challenge."),
        value_type=schema.TextLine(required=True),
        required=False,
        default=list(),
    )


class ITwoFactorLayer(Interface):
    """ A layer specific for this add-on product.
    """

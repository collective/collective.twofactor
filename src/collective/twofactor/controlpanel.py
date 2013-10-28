# -*- coding: utf-8 -*-

from collective.twofactor import _
from plone.app.registry.browser import controlpanel
from zope import schema
from zope.interface import Interface


class ITwilioSettings(Interface):
    """ Interface for the control panel form.
    """

    account_sid = schema.TextLine(
        title=_(u"Account SID"),
        description=_(u"Your Twilio Account SID."),
        required=True,
    )

    auth_token = schema.TextLine(
        title=_(u"Auth Token"),
        description=_(u"Your Twilio Auth Token."),
        required=True,
    )

    phone_number = schema.TextLine(
        title=_(u"Phone Number"),
        description=_(u"Your Twilio phone number from where to send SMS."),
        required=True,
    )


class TwilioSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ITwilioSettings
    label = _(u'Twilio Settings')
    description = _(u'Settings for configuring the Twilio SMS service')


class TwilioSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TwilioSettingsEditForm

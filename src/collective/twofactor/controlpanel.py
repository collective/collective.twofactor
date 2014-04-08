# -*- coding: utf-8 -*-

from collective.twofactor import _
from collective.twofactor.interfaces import ITwilioSettings
from collective.twofactor.interfaces import ITwoFactorSettings
from Products.statusmessages.interfaces import IStatusMessage
from plone.app.registry.browser import controlpanel
from twilio import TwilioRestException
from twilio.rest import TwilioRestClient
from z3c.form import button


class TwoFactorSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ITwoFactorSettings
    label = _(u'Two Factor Settings')
    description = _(u'Settings for the Two Factor authentication mechanism')


class TwilioSettingsEditForm(controlpanel.RegistryEditForm):
    schema = ITwilioSettings
    label = _(u'Twilio Settings')
    description = _(u'Settings for the Twilio SMS service')

    def validate_twilio_account(self, data):
        failure = False
        valid_phone = False

        client = TwilioRestClient(data['account_sid'], data['auth_token'])
        try:
            numbers = client.phone_numbers.list()
        except TwilioRestException as e:
            if e.status == 401:
                IStatusMessage(self.request).addStatusMessage(
                    _(u"The SID or token are invalid and we couldn't "
                      "authenticate with Twilio, please try again."),
                    "error")
            failure = True

        if not failure:
            for number in numbers:
                if number.phone_number == data['phone_number']:
                    valid_phone = True
                    break

            if not valid_phone:
                IStatusMessage(self.request).addStatusMessage(
                    _(u"The phone number you entered doesn't seem valid for "
                      "this Twilio account, please make sure you are "
                      "entering correctly."),
                    "error")
            else:
                if not number.capabilities.get('sms', False):
                    IStatusMessage(self.request).addStatusMessage(
                        _(u"The phone number entered is a valid Twilio number "
                          "for this account, however, this phone number "
                          "cannot send SMS. Please make sure to buy a phone "
                          "number which allows SMS to be sent."),
                        "error")
                    valid_phone = False

        return failure, valid_phone

    @button.buttonAndHandler(_('Save'), name='save')
    def handleSave(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        failure, valid_phone = self.validate_twilio_account(data)

        if not failure and valid_phone:
            self.applyChanges(data)
            IStatusMessage(self.request).addStatusMessage(_(u"Changes saved"),
                                                          "info")
            self.request.response.redirect("%s/%s" %
                                           (self.context.absolute_url(),
                                            self.control_panel_view))

    @button.buttonAndHandler(_('Cancel'), name='cancel')
    def handleCancel(self, action):
        IStatusMessage(self.request).addStatusMessage(_(u"Edit cancelled"),
                                                      "info")
        self.request.response.redirect("%s/%s" %
                                       (self.context.absolute_url(),
                                        self.control_panel_view))


class TwilioSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TwilioSettingsEditForm


class TwoFactorSettingsControlPanel(controlpanel.ControlPanelFormWrapper):
    form = TwoFactorSettingsEditForm

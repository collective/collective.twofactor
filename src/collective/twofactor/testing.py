# -*- coding: utf-8 -*-

from collective.twofactor.methods.base import LocalAuthentication
from collective.twofactor.methods.interfaces import ILocalAuthenticationMethod

from plone.app.testing import PloneSandboxLayer
from plone.app.testing import applyProfile
from plone.app.testing import PLONE_FIXTURE
from plone.app.testing import IntegrationTesting
from plone.app.testing import FunctionalTesting

from plone.testing import z2

from Products.CMFCore.interfaces import IMemberData
from Products.CMFCore.utils import getToolByName

from twilio import TwilioRestException
from twilio.rest import TwilioRestClient

from zope.component import getGlobalSiteManager
from zope.component.hooks import getSite
from zope.configuration import xmlconfig
from zope.publisher.interfaces.http import IHTTPRequest


class Messages:
    def __init__(self):
        pass

    def create(*args, **kwargs):
        if kwargs['to'] == '0':
            raise


class Sms:
    def __init__(self):
        self.messages = Messages()


class PhoneNumber:
    def __init__(self, number):
        self.phone_number = number

    @property
    def capabilities(self):
        if self.phone_number == 'no_sms_phone':
            return {'sms': False}
        elif self.phone_number == 'valid_phone':
            return {'sms': True}


class PhoneNumbers:
    def __init__(self, credentials=None):
        if credentials:
            self.sid = credentials[0]
            self.token = credentials[1]

    def list(self):
        if self.token == 'invalid_token':
            raise TwilioRestException(401, 'http://nohost/', "Test", 0)
        elif self.token == 'valid_token':
            return [PhoneNumber('no_sms_phone'), PhoneNumber('valid_phone')]


def twilio__init__(self, *args, **kwargs):
    self.sms = Sms()
    if len(args) > 1:
        self.sid = args[0]
        self.token = args[1]

        self.phone_numbers = PhoneNumbers(args)


def send(*args, **kwargs):
    if args[1] == 'should@fail.com':
        raise


class TestLocalAuth(LocalAuthentication):
    name = u"Test Authentication Adapter"

    valid_already_sent = u"Valid code already sent."
    new_code_sent = u"New code has been sent."
    error_sending = u"An error appeared"

    should_fail_sending = False

    def send_code(self):
        site = getSite()
        if self.should_fail_sending or site.REQUEST.get('should_fail'):
            self.failure = True
        else:
            # Override the local_code with a fixed one
            self.member.setProperties({'local_code': '12345678'})
            super(TestLocalAuth, self).send_code()


class CollectivetwofactorLayer(PloneSandboxLayer):

    defaultBases = (PLONE_FIXTURE,)

    def setUpZope(self, app, configurationContext):
        # Load ZCML
        import collective.twofactor
        xmlconfig.file(
            'configure.zcml',
            collective.twofactor,
            context=configurationContext
        )

        # Install products that use an old-style initialize() function
        #z2.installProduct(app, 'Products.PloneFormGen')

#    def tearDownZope(self, app):
#        # Uninstall products installed above
#        z2.uninstallProduct(app, 'Products.PloneFormGen')

    def setUpPloneSite(self, portal):
        applyProfile(portal, 'collective.twofactor:default')

        # Register our testing adapter
        gsm = getGlobalSiteManager()
        gsm.registerAdapter(TestLocalAuth,
                            (IMemberData, IHTTPRequest),
                            ILocalAuthenticationMethod,
                            'test')
        # Monkey-patch MailHost
        #import pdb;pdb.set_trace()
        mailhost = getToolByName(portal, 'MailHost')
        mailhost.send = send
        mailhost.smtp_host = 'localhost'
        portal.email_from_address = 'dummy@email.com'

        # Monkey-path TwilioRestClient
        TwilioRestClient.__init__ = twilio__init__


COLLECTIVE_TWOFACTOR_FIXTURE = CollectivetwofactorLayer()
COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING = IntegrationTesting(
    bases=(COLLECTIVE_TWOFACTOR_FIXTURE,),
    name="CollectivetwofactorLayer:Integration"
)
COLLECTIVE_TWOFACTOR_FUNCTIONAL_TESTING = FunctionalTesting(
    bases=(COLLECTIVE_TWOFACTOR_FIXTURE, z2.ZSERVER_FIXTURE),
    name="CollectivetwofactorLayer:Functional"
)

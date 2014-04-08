# -*- coding: utf-8 -*-

from archetypes.schemaextender.field import ExtensionField
from archetypes.schemaextender.interfaces import ISchemaExtender
from plone.app.users.browser.personalpreferences import UserDataPanelAdapter
from Products.Archetypes import public as atapi
try:  # pragma: no cover
    from Products.remember.interfaces import IReMember
    from Products.remember.content.member import Member
    REMEMBER = True
except:
    REMEMBER = False
from zope.component import adapts
from zope.component import getUtility
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """
    def get_two_factor_method(self):
        return self.context.getProperty('two_factor_method', '')

    def set_two_factor_method(self, value):
        # Not only save the method, but also remove the session hash and any
        # old local code
        if not value:
            value = ''
        return self.context.setMemberProperties({'two_factor_hash': '',
                                                 'two_factor_hash_date': '',
                                                 'local_code': '',
                                                 'local_code_date': '',
                                                 'local_code_sent': False,
                                                 'two_factor_method': value})

    two_factor_method = property(get_two_factor_method, set_two_factor_method)

    def get_cell_phone(self):
        return self.context.getProperty('cell_phone', '')

    def set_cell_phone(self, value):
        return self.context.setMemberProperties({'cell_phone': value})

    cell_phone = property(get_cell_phone, set_cell_phone)


if REMEMBER:  # pragma: no cover
    class MyStringField(ExtensionField, atapi.StringField):
        """A trivial field."""

        def getMutator(self, instance):
            return getattr(instance, self.mutator)

    class MyBooleanField(ExtensionField, atapi.BooleanField):
        """A trivial field."""

    class MemberExtender(object):
        adapts(IReMember)
        implements(ISchemaExtender)

        fields = [
            MyStringField(
                'two_factor_method',
                default='',
                mode='rw',
                accessor='getTwoFactorMethod',
                mutator='setTwoFactorMethod',
                user_property=True,
                required=False,
                vocabulary="getTwoFactorMethods",
                widget=atapi.SelectionWidget(
                    label=u'Two-factor authentication method',
                    label_msgid='two_factor_method',
                    description=(u"Choose the method you would like to use "
                                 "for Two-factor authentication"),
                    description_msgid='help_two_factor_method',
                    format='select',
                    i18n_domain='collective.twofactor',
                )
            ),
            MyStringField(
                'cell_phone',
                mode='rw',
                accessor='getCellPhone',
                mutator='setCellPhone',
                user_property=True,
                widget=atapi.StringWidget(
                    label=u'Cell phone number',
                    label_msgid='label_cell_phone',
                    description=(u"Enter your phone number if you choose to "
                                 "receive a code by SMS. Please use "
                                 "international format. Example: "
                                 "+15555555555"),
                    description_msgid='help_cell_phone',
                    i18n_domain='collective.twofactor')
            ),
            MyStringField(
                'two_factor_hash',
                accessor='getTwoFactorHash',
                mutator='setTwoFactorHash',
                mode='rw',
                user_property=True,
                widget=atapi.StringWidget(
                    visible={'view': 'invisible', 'edit': 'invisible'},
                )
            ),
            MyStringField(
                'two_factor_hash_date',
                accessor='getTwoFactorHashDate',
                mutator='setTwoFactorHashDate',
                mode='rw',
                user_property=True,
                widget=atapi.StringWidget(
                    visible={'view': 'invisible', 'edit': 'invisible'},
                )
            ),
            MyStringField(
                'local_code',
                accessor='getLocalCode',
                mutator='setLocalCode',
                mode='rw',
                user_property=True,
                widget=atapi.StringWidget(
                    visible={'view': 'invisible', 'edit': 'invisible'},
                )
            ),
            MyStringField(
                'local_code_date',
                accessor='getLocalCodeDate',
                mutator='setLocalCodeDate',
                mode='rw',
                user_property=True,
                widget=atapi.StringWidget(
                    visible={'view': 'invisible', 'edit': 'invisible'},
                )
            ),
            MyBooleanField(
                'local_code_sent',
                mode='rw',
                accessor='getLocalCodeSent',
                mutator='setLocalCodeSent',
                user_property=True,
                widget=atapi.BooleanWidget(
                    visible={'view': 'invisible', 'edit': 'invisible'},
                )
            ),
        ]

        def __init__(self, context):
            self.context = context

        def getFields(self):
            return self.fields

    def validate(self, *args, **kwargs):
        errors = self._original_validate(*args, **kwargs)

        request = kwargs['REQUEST']
        if (request.get('two_factor_method') and
                request.get('two_factor_method') == 'sms'):
            if not request.get('cell_phone'):
                errors['cell_phone'] = (
                    "You need to provide a cell phone if you choose to use "
                    "the two-factor authentication through SMS"
                )

        return errors

    def getTwoFactorMethod(self):
        return self.getUser().getProperty('two_factor_method', None)

    def setTwoFactorMethod(self, value):
        # Not only save the method, but also remove the session hash and any
        # old local code
        self.getUser().getField('two_factor_method').set(self, value)
        self.getUser().getField('two_factor_hash').set(self, None)
        self.getUser().getField('two_factor_hash_date').set(self, None)
        self.getUser().getField('local_code').set(self, None)
        self.getUser().getField('local_code_date').set(self, None)
        self.getUser().getField('local_code_sent').set(self, None)

    def getCellPhone(self):
        return self.getUser().getProperty('cell_phone', '')

    def setCellPhone(self, value):
        self.getUser().getField('cell_phone').set(self, value)

    def getTwoFactorMethods(self):
        values = []
        factory = getUtility(IVocabularyFactory,
                             "collective.twofactor.methods")
        for term in factory(self):
            values.append((term.token, term.title))
        return values

    def getTwoFactorHash(self):
        return self.getUser().getProperty('two_factor_hash', '')

    def setTwoFactorHash(self, value):
        self.getUser().getField('two_factor_hash').set(self, value)

    def getTwoFactorHashDate(self):
        return self.getUser().getProperty('two_factor_hash_date', '')

    def setTwoFactorHashDate(self, value):
        self.getUser().getField('two_factor_hash_date').set(self, value)

    def getLocalCode(self):
        return self.getUser().getProperty('local_code', '')

    def setLocalCode(self, value):
        self.getUser().getField('local_code').set(self, value)

    def getLocalCodeDate(self):
        return self.getUser().getProperty('local_code_date', '')

    def setLocalCodeDate(self, value):
        self.getUser().getField('local_code_date').set(self, value)

    def getLocalCodeSent(self):
        return self.getUser().getProperty('local_code_sent', '')

    def setLocalCodeSent(self, value):
        self.getUser().getField('local_code_sent').set(self, value)

    Member.getTwoFactorMethod = getTwoFactorMethod
    Member.setTwoFactorMethod = setTwoFactorMethod
    Member.getTwoFactorMethods = getTwoFactorMethods
    Member.getCellPhone = getCellPhone
    Member.setCellPhone = setCellPhone
    Member.getTwoFactorHash = getTwoFactorHash
    Member.setTwoFactorHash = setTwoFactorHash
    Member.getTwoFactorHashDate = getTwoFactorHashDate
    Member.setTwoFactorHashDate = setTwoFactorHashDate
    Member.getLocalCode = getLocalCode
    Member.setLocalCode = setLocalCode
    Member.getLocalCodeDate = getLocalCodeDate
    Member.setLocalCodeDate = setLocalCodeDate
    Member.getLocalCodeSent = getLocalCodeSent
    Member.setLocalCodeSent = setLocalCodeSent
    Member._original_validate = Member.validate
    Member.validate = validate

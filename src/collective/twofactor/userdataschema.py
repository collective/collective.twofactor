# -*- coding: utf-8 -*-

from collective.twofactor import _
from plone.app.users.userdataschema import IUserDataSchema
from plone.app.users.userdataschema import IUserDataSchemaProvider
from zope.interface import implements
from zope import schema


class IEnhancedUserDataSchema(IUserDataSchema):
    """ Use all the fields from the default user data schema, and add various
    extra fields.
    """

    two_factor_method = schema.Choice(
        title=_(u'two_factor_method',
                default=u'Two-factor authentication method'),
        description=_(u'help_two_factor_method',
                      default=(u"Choose the method you would like to use for "
                               "Two-factor authentication")),
        vocabulary="collective.twofactor.methods",
        required=False,
        )

    cell_phone = schema.TextLine(
        title=_(u'label_cell_phone', default=u'Cell phone number'),
        description=_(u'help_cell_phone',
                      default=(u"Enter your phone number if you choose to "
                               "receive a code by SMS. Please use "
                               "international format. Example: +15555555555")),
        required=False,
        )


class UserDataSchemaProvider(object):
    implements(IUserDataSchemaProvider)

    def getSchema(self):
        """
        """
        return IEnhancedUserDataSchema

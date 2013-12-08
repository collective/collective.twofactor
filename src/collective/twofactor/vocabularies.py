# -*- coding: utf-8 -*-

from collective.twofactor.adapter import EnhancedUserDataPanelAdapter
from collective.twofactor.methods.interfaces import IAuthenticationMethod
from zope.component import getAdapters
from zope.interface import implements
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleVocabulary
from zope.schema.vocabulary import SimpleTerm
from Products.CMFCore.utils import getToolByName


class TwoFactorMethodsVocabulary(object):
    implements(IVocabularyFactory)

    def __call__(self, context):
        if isinstance(context, EnhancedUserDataPanelAdapter):
            mem = context.context
        else:
            mt = getToolByName(context, 'portal_membership')
            mem = mt.getAuthenticatedMember()

        methods = []
        for method in getAdapters((mem,), IAuthenticationMethod):
            methods.append(SimpleTerm(value=method[0], title=method[1].name))

        return SimpleVocabulary(methods)

TwoFactorMethodsVocabularyFactory = TwoFactorMethodsVocabulary()

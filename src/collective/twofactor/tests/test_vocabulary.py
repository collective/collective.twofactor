# -*- coding: utf-8 -*-

import unittest2 as unittest

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory


class TestVocabulary(unittest.TestCase):

    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']

    def test_vocabulary_list_all_adapters(self):
        factory = getUtility(IVocabularyFactory,
                             "collective.twofactor.methods")
        vocabulary = factory(self.portal)
        terms = [i.token for i in vocabulary._terms]

        self.assertListEqual(terms, ['test', 'sms', 'email'])

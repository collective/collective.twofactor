# -*- coding: utf-8 -*-

import unittest2 as unittest

from collective.twofactor.userdataschema import IEnhancedUserDataSchema

from Products.CMFCore.utils import getToolByName

from collective.twofactor.testing import \
    COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING


class TestMemberAdapt(unittest.TestCase):

    layer = COLLECTIVE_TWOFACTOR_INTEGRATION_TESTING

    def setUp(self):
        self.app = self.layer['app']
        self.portal = self.layer['portal']
        self.pm_tool = getToolByName(self.portal, 'portal_membership')
        self.adapter = IEnhancedUserDataSchema(self.portal)
        self.member = self.pm_tool.getAuthenticatedMember()

    def test_reset_properties_on_setting_two_factor_method(self):
        self.member.setMemberProperties({'two_factor_hash': '1',
                                         'two_factor_hash_date': '2',
                                         'local_code': '3',
                                         'local_code_date': '4',
                                         'local_code_sent': True,
                                         'two_factor_method': '5'})

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code = self.member.getProperty('local_code')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        two_factor_method = self.member.getProperty('two_factor_method')

        self.assertEqual(two_factor_hash, '1')
        self.assertEqual(two_factor_hash_date, '2')
        self.assertEqual(local_code, '3')
        self.assertEqual(local_code_date, '4')
        self.assertTrue(local_code_sent)
        self.assertEqual(two_factor_method, '5')

        self.adapter.two_factor_method = 'email'

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code = self.member.getProperty('local_code')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        two_factor_method = self.adapter.two_factor_method

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)
        self.assertEqual(two_factor_method, 'email')

        self.member.setMemberProperties({'two_factor_hash': '1',
                                         'two_factor_hash_date': '2',
                                         'local_code': '3',
                                         'local_code_date': '4',
                                         'local_code_sent': True,
                                         'two_factor_method': '5'})

        self.adapter.two_factor_method = None

        two_factor_hash = self.member.getProperty('two_factor_hash')
        two_factor_hash_date = self.member.getProperty('two_factor_hash_date')
        local_code = self.member.getProperty('local_code')
        local_code_date = self.member.getProperty('local_code_date')
        local_code_sent = self.member.getProperty('local_code_sent')
        two_factor_method = self.adapter.two_factor_method

        self.assertEqual(two_factor_hash, '')
        self.assertEqual(two_factor_hash_date, '')
        self.assertEqual(local_code, '')
        self.assertEqual(local_code_date, '')
        self.assertFalse(local_code_sent)
        self.assertEqual(two_factor_method, '')

    def test_cell_phone_accesor_and_mutator(self):
        self.member.setMemberProperties({'cell_phone': ''})

        cell_phone = self.adapter.cell_phone

        self.assertEqual(cell_phone, '')

        self.adapter.cell_phone = '123456789'

        cell_phone = self.adapter.cell_phone

        self.assertEqual(cell_phone, '123456789')

        cell_phone = self.member.getProperty('cell_phone')

        self.assertEqual(cell_phone, '123456789')

    def test_two_factor_method_accesor_and_mutator(self):
        self.member.setMemberProperties({'two_factor_method': ''})

        two_factor_method = self.adapter.two_factor_method

        self.assertEqual(two_factor_method, '')

        self.adapter.two_factor_method = 'test-method'

        two_factor_method = self.adapter.two_factor_method

        self.assertEqual(two_factor_method, 'test-method')

        two_factor_method = self.member.getProperty('two_factor_method')

        self.assertEqual(two_factor_method, 'test-method')

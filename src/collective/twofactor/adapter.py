# -*- coding: utf-8 -*-

from plone.app.users.browser.personalpreferences import UserDataPanelAdapter


class EnhancedUserDataPanelAdapter(UserDataPanelAdapter):
    """
    """

    def get_two_factor_method(self):
        return self.context.getProperty('two_factor_method', '')
    def set_two_factor_method(self, value):
        # Not only save the method, but also remove the session hash and any
        # old local code
        return self.context.setMemberProperties({'two_factor_hash': None,
                                                 'two_factor_hash_date': None,
                                                 'local_code': None,
                                                 'local_code_date': None,
                                                 'local_code_sent': False,
                                                 'two_factor_method': value})
    two_factor_method = property(get_two_factor_method, set_two_factor_method)

    def get_cell_phone(self):
        return self.context.getProperty('cell_phone', '')
    def set_cell_phone(self, value):
        return self.context.setMemberProperties({'cell_phone': value})
    cell_phone = property(get_cell_phone, set_cell_phone)

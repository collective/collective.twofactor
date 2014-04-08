import logging

from Products.CMFCore.utils import getToolByName


def upgrade_from_1_to_2(context, logger=None):
    if logger is None:
        # Called as upgrade step: define our own logger.
        logger = logging.getLogger('collective.twofactor')

    logger.info("Checking all site members to see if they have enabled sms "
                "auth, but did not provide a cell_phone")
    mt = getToolByName(context, 'portal_membership')
    for member in mt.listMembers():
        if member.getProperty('two_factor_method') == 'sms':
            if not member.getProperty('cell_phone'):
                member.setMemberProperties({'two_factor_hash': '',
                                            'two_factor_hash_date': '',
                                            'local_code': '',
                                            'local_code_date': '',
                                            'local_code_sent': False,
                                            'two_factor_method': ''})

                logger.info("Fixed user %s" % member.id)

    logger.info("All done.")

# -*- coding: utf-8 -*-
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.CMFCore.utils import getToolByName

from plugin.logout import addClearTwoFactorPlugin

import logging


logger = logging.getLogger("collective.twofactor")


def importVarious(context):
    """ Install the Clear Two Factor Session Plugin
    """

    portal = context.getSite()

    uf = getToolByName(portal, 'acl_users')
    installed = uf.objectIds()

    if 'twofactor' not in installed:
        addClearTwoFactorPlugin(uf, 'twofactor', 'Example PAS')
        activatePluginInterfaces(portal, 'twofactor')
        logging.info("Clear Two Factor Session Plugin installed successfully")
    else:
        logging.info("Clear Two Factor Session Plugin was already installed")

    logging.info("Done.")

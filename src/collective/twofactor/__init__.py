# -*- coding: utf-8 -*-
from Products.PluggableAuthService.PluggableAuthService import registerMultiPlugin
from plugin.logout import addClearTwoFactorPlugin
from plugin.logout import ClearTwoFactorPlugin
from plugin.logout import manage_addClearTwoFactorPluginForm

from zope.i18nmessageid import MessageFactory
_ = MessageFactory("collective.twofactor")


def initialize(context):
    """Initializer called when used as a Zope 2 product."""

    registerMultiPlugin(ClearTwoFactorPlugin.meta_type)  # Add to PAS menu
    context.registerClass(ClearTwoFactorPlugin,
                          constructors=(manage_addClearTwoFactorPluginForm,
                                        addClearTwoFactorPlugin),
                          visibility = None)

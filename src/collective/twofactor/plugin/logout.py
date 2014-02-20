from Products.PluggableAuthService.plugins.BasePlugin import BasePlugin
from AccessControl.SecurityInfo import ClassSecurityInfo
from Products.PluggableAuthService.utils import classImplements
from Globals import InitializeClass
from Products.PluggableAuthService.interfaces.plugins import \
    ICredentialsResetPlugin
from Products.CMFCore.utils import getToolByName
from Products.PageTemplates.PageTemplateFile import PageTemplateFile

from collective.twofactor.methods.interfaces import IAuthenticationMethod

from zope.component import getMultiAdapter


manage_addClearTwoFactorPluginForm = PageTemplateFile(
    'www/addClearTwoFactorPAS',
    globals(),
    __name__='manage_addClearTwoFactorPluginForm'
)


def addClearTwoFactorPlugin(self, id, title='', REQUEST=None):
    """ Add the plugin to Plone PAS
    """
    o = ClearTwoFactorPlugin(id, title)
    self._setObject(o.getId(), o)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect(
            '%s/manage_main'
            '?manage_tabs_message=Clear+Two+Factor+Session+Plugin+added.' %
            self.absolute_url())


class ClearTwoFactorPlugin(BasePlugin):
    """ Plugin for Clearing the two factor session when logging out
    """
    meta_type = 'Clear Two Factor Session Plugin'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title

    # ICredentialsResetPlugin implementation
    def resetCredentials(self, request, response):
        mt = getToolByName(self, 'portal_membership')
        member = mt.getAuthenticatedMember()
        method = member.getProperty('two_factor_method', None)
        if method:
            auth = getMultiAdapter((member, request),
                                   IAuthenticationMethod,
                                   name=method)
            auth.clear_session()


classImplements(ClearTwoFactorPlugin, ICredentialsResetPlugin)
InitializeClass(ClearTwoFactorPlugin)

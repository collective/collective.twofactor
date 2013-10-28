import binascii
import logging
from AccessControl.SecurityInfo import ClassSecurityInfo
from Globals import InitializeClass
from plone.session.plugins.session import SessionPlugin
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from Products.PluggableAuthService.utils import classImplements
from Products.PluggableAuthService.interfaces.plugins import IAuthenticationPlugin
from Products.PluggableAuthService.interfaces.plugins import ICredentialsResetPlugin
from Products.PluggableAuthService.interfaces.plugins import IExtractionPlugin
from Products.PluggableAuthService.interfaces.plugins import IChallengePlugin


manage_addTwoFactorPluginForm = PageTemplateFile('www/addTwoFactorPAS',
    globals(), __name__='manage_addTwoFactorPluginForm')


logger = logging.getLogger("collective.twofactor")


def addTwoFactorPlugin(self, id, title='', REQUEST=None):
    """ Add a Two-factor PAS Plugin to Plone PAS
    """
    o = TwoFactorPlugin(id, title)
    self._setObject(o.getId(), o)

    if REQUEST is not None:
        REQUEST['RESPONSE'].redirect('%s/manage_main'
            '?manage_tabs_message=TwoFactor+PAS+Plugin+added.' %
            self.absolute_url())


class TwoFactorPlugin(SessionPlugin):
    """ Plugin for TwoFactor PAS
    """
    meta_type = 'TwoFactor PAS'
    security = ClassSecurityInfo()

    def __init__(self, id, title=None):
        self._setId(id)
        self.title = title
        self.valid_user = False

    # IAuthenticationPlugin implementation
    def authenticateCredentials(self, credentials):
        """ Authenticate credentials based on the user choice for a two-factor
        authentication method
        """

        import pdb;pdb.set_trace()
  
        ticket=credentials["cookie"]
        ticket_data = self._validateTicket(ticket)
        if ticket_data is None:
            return None
        (digest, userid, tokens, user_data, timestamp) = ticket_data
        pas=self._getPAS()
        info=pas._verifyUser(pas.plugins, user_id=userid)
        if info is None:
            return None

        # XXX Should refresh the ticket if after timeout refresh.
        return (info['id'], info['login'])

        if 'login' not in credentials or 'password' not in credentials:
            return None

        users = {'foo' : 'bar'}

        login = credentials['login']
        password = credentials['password']

        if users.get(login, None) == password:
            self._getPAS().updateCredentials(self.REQUEST,
                self.REQUEST.RESPONSE, login, password)
            return (login, login)

        return None

    # IExtractionPlugin implementation
    def extractCredentials(self, request):
        logger.debug("extractCredentials")
        creds={}

        if not self.cookie_name in request:
            # If no cookie, extract credentials from the request
            logger.debug("No cookie present, extracting from REQUEST")
  
            creds[ 'login' ] = request.get('__ac_name', None)
            creds[ 'password' ] = request.get('__ac_password', None)
            creds[ 'twofactor_token' ] = request.get('two_factor_token', None)
        
        else:
            try:
                creds["cookie"]=binascii.a2b_base64(request.get(self.cookie_name))
            except binascii.Error:
                # If we have a cookie which is not properly base64 encoded it
                # can not be ours.
                return creds

        creds["source"]="collective.twofactor"

        return creds

    # ICredentialsUpdatePlugin implementation
    def updateCredentials(self, request, response, login, new_password):
        pas=self._getPAS()
        info=pas._verifyUser(pas.plugins, login=login)
        if info is not None:
            # Only setup a session for users in our own user folder.
            self._setupSession(info["id"], response)
            #self._setupSession(self, userid, response, tokens=(), user_data=''):

    # IChallengePlugin implementation
    def challenge( self, request, response, **kw ):
        import pdb;pdb.set_trace()
        realm = response.realm
        if realm:
            response.addHeader('WWW-Authenticate',
                               'basic realm="%s"' % realm)
        m = "<strong>You are not authorized to access this resource.</strong>"

        response.setBody(m, is_error=1)
        response.setStatus(401)
        return 1


classImplements(TwoFactorPlugin, IExtractionPlugin, IAuthenticationPlugin,
                ICredentialsResetPlugin, IChallengePlugin)
InitializeClass(TwoFactorPlugin)
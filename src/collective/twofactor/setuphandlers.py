from pas_plugin import addTwoFactorPlugin
from Products.PlonePAS.Extensions.Install import activatePluginInterfaces
from Products.CMFCore.utils import getToolByName
from StringIO import StringIO


def importVarious(context):
    """ Install the Two-factor PAS plugin
    """
    
    out = StringIO()
    portal = context.getSite()

    uf = getToolByName(portal, 'acl_users')
    installed = uf.objectIds()

    if 'twofactorpas' not in installed:
        addTwoFactorPlugin(uf, 'twofactorpas', 'TwoFactor PAS')
        activatePluginInterfaces(portal, 'twofactorpas', out)
    else:
        print >> out, 'twofactorpas already installed'

    print out.getvalue()

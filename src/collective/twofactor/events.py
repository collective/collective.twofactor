# -*- coding: utf-8 -*-

from collective.twofactor.interfaces import ITwoFactorSettings
from collective.twofactor.methods.interfaces import IAuthenticationMethod
from zope.component import getMultiAdapter
from plone import api
from Products.CMFCore.utils import getToolByName
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def check_valid_session(event):

    # Should we check a valid session hash in this request ?
    should_check = True
    try:
        registry = getUtility(IRegistry)
        settings = registry.forInterface(ITwoFactorSettings)
    except:
        # By a different number of reasons, we might not be able to get the
        # registry settings.
        # Just ignore and do not do any validation
        return

    for i in settings.to_ignore:
        if event.request.get('PATH_INFO').endswith(i):
            should_check = False

    if should_check:
        try:
            portal = api.portal.get()
        except:  # pragma: no cover
            # If we cannot get the portal, then just return and ignore
            return
        mt = getToolByName(portal, 'portal_membership')
        member = mt.getAuthenticatedMember()

        method = member.getProperty('two_factor_method', None)
        if method:
            auth = getMultiAdapter((member, member.REQUEST),
                                   IAuthenticationMethod,
                                   name=method)
            if not auth.is_valid_session():
                portal_url = portal.absolute_url()
                url = ("%s/two-factor-challenge?came_from=%s" %
                       (portal_url, event.request.get('URL')))

                event.request.response.redirect(url)

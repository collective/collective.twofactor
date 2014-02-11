# -*- coding: utf-8 -*-

from collective.twofactor.methods.interfaces import IAuthenticationMethod
from zope.component import getMultiAdapter
from plone import api
from Products.CMFCore.utils import getToolByName


def check_valid_session(event):

    # Should we check a valid session hash in this request ?
    should_check = True

    # Ignore common resources and the "two-factor-challenge" view.
    to_ignore = ['two-factor-challenge',
                 # XXX: Exclude the personal preferences until we can
                 # provide cell phone validation before saving.
                 '@@personal-information',
                 'logout',
                 '.css',
                 '.js',
                 '.png',
                 '.jpg',
                 '.gif',
                 '.ico',
                 ]
    for i in to_ignore:
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

# -*- coding: utf-8 -*-

from collective.twofactor import _
from collective.twofactor.methods.interfaces import IAuthenticationMethod
from plone.memoize.instance import memoize
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import queryAdapter


class TwoFactorChallengeView(BrowserView):
    """
    """

    def auth_status(self):
        return self.auth.status.get('message', u"")

    def could_send_code(self):
        could_send = True
        status = self.auth.status.get('status', u'success')
        if status == u'error':
            could_send = False

        return could_send

    def __call__(self):
        mt = getToolByName(self.context, 'portal_membership')

        member = mt.getAuthenticatedMember()
        method = member.getProperty('two_factor_method', None)

        self.auth = queryAdapter(member, IAuthenticationMethod, name=method)

        if self.auth:
            status = u""
            if 'submit' in self.request:
                came_from = self.request.get('came_from', None)
                code = self.request.get("two-factor-token", None)
                if code and self.auth.valid_code(code):
                    self.auth.generate_session_hash()
                    if came_from:
                        if came_from.endswith('/login_form'):
                            came_from = came_from.replace('/login_form', '/logged_in')
                        self.request.response.redirect(came_from)
                    else:
                        self.request.response.redirect(self.context.absolute_url())
                else:
                    self.request.set('came_from', came_from)
                    status = _(u"The code you entered is invalid, please try again.")

            elif 'reset_code' in self.request:
                self.auth.reset_code()

            else:
                self.auth.execute()

            return self.index(status=status)

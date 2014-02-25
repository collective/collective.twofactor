# -*- coding: utf-8 -*-

from collective.twofactor import _
from collective.twofactor.methods.interfaces import IAuthenticationMethod
from Products.CMFCore.utils import getToolByName
from Products.Five.browser import BrowserView
from zope.component import queryMultiAdapter


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

        self.auth = queryMultiAdapter((member, self.request),
                                      IAuthenticationMethod,
                                      name=method)

        if self.auth:
            status = u""
            if 'submit' in self.request:
                came_from = self.request.get('came_from', None)
                code = self.request.get("two-factor-token", None)
                if code and self.auth.valid_code(code):
                    self.auth.generate_session_hash()
                    if came_from:
                        login_templates = [
                            '/login_form',
                            '/logged_out',
                            '/login_failed',
                        ]
                        for template in login_templates:
                            if came_from.endswith(template):
                                came_from = came_from.replace(template,
                                                              '/logged_in')
                                break
                        self.request.response.redirect(came_from)
                    else:
                        self.request.response.redirect(
                            self.context.absolute_url()
                        )
                else:
                    self.request.set('came_from', came_from)
                    status = _(u"The code you entered is invalid, please try "
                               "again.")

            elif 'reset_code' in self.request:
                self.auth.reset_code()

            else:
                self.auth.execute()

            return self.index(status=status)

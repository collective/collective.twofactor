# -*- coding: utf-8 -*-
from datetime import datetime
from hashlib import sha256
from random import random

from collective.twofactor.config import SESSION_VALID
from collective.twofactor.config import LOCAL_CODE_VALID
from interfaces import IAuthenticationMethod
from interfaces import ILocalAuthenticationMethod
from zope.interface import implements


class BaseAuthentication(object):
    implements(IAuthenticationMethod)
    
    name = ""
    failure = False
    
    def __init__(self, member):
        self.member = member
        self.status = {}
        
    def generate_session_hash(self):
        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        member_id = self.member.id
        h = sha256("%s%s" % (member_id, current_time)).hexdigest()
        self.member.setProperties({'two_factor_hash': h,
                                   'two_factor_hash_date': current_time})

    def is_valid_session(self):
        valid = False

        session_hash = self.member.getProperty('two_factor_hash', None)
        session_hash_date = self.member.getProperty('two_factor_hash_date', None)

        if session_hash and session_hash_date:
            hash_date = datetime.strptime(session_hash_date, "%Y-%m-%dT%H:%M:%S")
            member_id = self.member.id
            h = sha256("%s%s" % (member_id, session_hash_date)).hexdigest()

            current_time = datetime.now()
            delta = current_time - hash_date

            if session_hash == h and delta.seconds < SESSION_VALID:
                valid = True

        return valid

    def valid_code(self, code):
        # Override this method for your specific method
        return False

    def execute(self):
        # Intended to be overriden by a subclass to execute specific code
        # needed to be ran before requesting the auth code.
        pass


class LocalAuthentication(BaseAuthentication):
    """ Intended to be subclassed for authentication methods which generate
    a local code and send it to the user somehow
    """
    implements(ILocalAuthenticationMethod)

    valid_already_sent = u""
    new_code_sent = u""
    error_sending = u""

    def generate_random_code(self, length=8):
        random_code = 0
        while random_code < 10**(length-1):
            # Make sure the generated code has 'length' length.
            random_code = str(int(random()*(10**length)))

        current_time = datetime.now().strftime("%Y-%m-%dT%H:%M:%S")
        self.member.setProperties({'two_factor_hash': '',
                                   'two_factor_hash_date': '',
                                   'local_code': random_code,
                                   'local_code_date': current_time,
                                   'local_code_sent': False,
                                   })

    def valid_code(self, code):
        valid = False

        local_code = self.member.getProperty('local_code', None)
        local_code_date = self.member.getProperty('local_code_date', None)

        if local_code:
            code_date = datetime.strptime(local_code_date, "%Y-%m-%dT%H:%M:%S")

            current_time = datetime.now()
            delta = current_time - code_date

            if code == local_code and delta.seconds < LOCAL_CODE_VALID:
                valid = True

        return valid
      
    def get_code(self):
        return self.member.getProperty('local_code', None)

    def send_code(self):
        # Override this method with your specific authentication method, and
        # make sure to call this method from the superclass.
        self.member.setProperties({'local_code_sent': True})

    def reset_code(self):
        self.generate_random_code()
        self.send_code()
        if self.failure:
            self.member.setProperties({'two_factor_hash': '',
                                        'two_factor_hash_date': '',
                                        'local_code': '',
                                        'local_code_date': '',
                                        'local_code_sent': False,
                                      })
            self.status['message'] = self.error_sending
            self.status['status'] = u'error'
        else:
            self.status['message'] = self.new_code_sent
            self.status['status'] = u'success'

    def execute(self):
        valid = False

        local_code = self.member.getProperty('local_code', None)
        local_code_date = self.member.getProperty('local_code_date', None)
        local_code_sent = self.member.getProperty('local_code_sent', False)
        
        if local_code:
            code_date = datetime.strptime(local_code_date, "%Y-%m-%dT%H:%M:%S")

            current_time = datetime.now()
            delta = current_time - code_date

            if delta.seconds < LOCAL_CODE_VALID:
                valid = True

        if valid and local_code_sent:
            self.status['message'] = self.valid_already_sent
            self.status['status'] = u'success'
            
        elif not valid:
            self.generate_random_code()
            self.send_code()
            if self.failure:
                self.member.setProperties({'two_factor_hash': '',
                                           'two_factor_hash_date': '',
                                           'local_code': '',
                                           'local_code_date': '',
                                           'local_code_sent': False,
                                          })
                self.status['message'] = self.error_sending
                self.status['status'] = u'error'
            else:
                self.status['message'] = self.new_code_sent
                self.status['status'] = u'success'

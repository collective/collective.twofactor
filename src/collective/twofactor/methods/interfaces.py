# -*- coding: utf-8 -*-

from zope.interface import Interface


class IAuthenticationMethod(Interface):
    """ Base interface for authentication methods
    """

    def generate_session_hash():
        """ Generates a session for the current member which is valid for
        certain amount of time, in which he is not asked again for the
        auth token.
        """

    def is_valid_session():
        """ Checks wether the current member has a valid session already
        """

    def valid_code(code):
        """ Checks wether the entered code is valid
        """

    def execute():
        """ Execute whatever is needed before rendering the challenge view.
        This method is intended to be overriden by your local method
        implementation
        """
  

class ILocalAuthenticationMethod(IAuthenticationMethod):
    """ Methods that save a local code and send it to the user should provide
    this interface
    """

    def generate_random_code(length):
        """ Generate a random code of 'length' length
        """
      
    def get_code():
        """ Gets the local code
        """

    def send_code():
        """ Sends the local code. This method is intended to be overriden
        by your local method implementation
        """

    def reset_code():
        """ Generate a new random code and send it
        """

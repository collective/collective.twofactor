from collective.twofactor.testing import\
    COLLECTIVE_TWOFACTOR_FUNCTIONAL_TESTING
from plone.testing import layered
import robotsuite
import unittest


def test_suite():
    suite = unittest.TestSuite()
    suite.addTests([
        layered(robotsuite.RobotTestSuite("twilio_controlpanel.txt"),
                layer=COLLECTIVE_TWOFACTOR_FUNCTIONAL_TESTING)
    ])
    suite.addTests([
        layered(robotsuite.RobotTestSuite("test_twofactor.txt"),
                layer=COLLECTIVE_TWOFACTOR_FUNCTIONAL_TESTING)
    ])
    return suite

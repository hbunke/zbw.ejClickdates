#from Products.Five import zcml
from Products.Five import fiveconfigure
from Testing import ZopeTestCase as ztc
from Products.PloneTestCase import PloneTestCase as ptc
from Products.PloneTestCase.layer import PloneSite

import zbw.ejClickdates


class layer(PloneSite):
    
    @classmethod
    def setUp(cls):
        fiveconfigure.debug_mode = True
        ztc.installPackage(zbw.ejClickdates)
        fiveconfigure.debug_mode = False

    @classmethod
    def tearDown(cls):
        pass

ptc.setupPloneSite()


class ZopeTest(ztc.ZopeTestCase):
    """no plone overhead
    """


class PloneTest(ptc.PloneTestCase):
    """We use this base class for all the tests in this package. If necessary,
    we can put common utility or setup code in here. This applies to unit 
    test cases.
    """

class FunctionalTestCase(ptc.FunctionalTestCase):
    """We use this class for functional integration tests that use doctest
    syntax. Again, we can put basic common utility or setup code in here.
    """
    #def __init__(self):
    #    self.request = self.portal.REQUEST


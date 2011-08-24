# -*- coding: UTF-8 -*-

# Dr. Hendrik Bunke <h.bunke@zbw.eu>
# German National Library of Economics


import unittest
from zbw.ejClickdates.tests.base import PloneTest
from zbw.ejClickdates.interfaces import IClickdates, IClickdatesAnnotatable
from zope.app.annotation.interfaces import IAnnotations
from zope.interface import implements
import datetime


ANNOTATION = "hbxt.clickdates"

class Dummy(object):
    """ 
    Dummy object for storing annotation
    """
    implements(IClickdatesAnnotatable)


class ClickdateAnnotationTest(PloneTest):
    """
    test for adapter
    """

    def afterSetUp(self):
        self.obj = Dummy()
        self.dan = IClickdates(self.obj)
        self.dan.clickDate()
        self.thisMonth = datetime.date.today().month
        self.thisYear = datetime.date.today().year
        self.annotations = IAnnotations(self.obj)
        self.date = "%s-%s" %(self.thisYear, self.thisMonth)


    def test_annotation(self):
        self.assertTrue(self.annotations.has_key(ANNOTATION))

    def test_month_key(self):
        key = self.annotations[ANNOTATION]
        self.assertTrue(key.has_key(self.date))
    
    def test_date(self):
        key = self.annotations[ANNOTATION][self.date]
        clickdate = key[0]
        self.assertEqual(clickdate.year, self.thisYear)
        self.assertEqual(clickdate.month, self.thisMonth)
        #XXX should we test time as well...?



def test_suite():
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite((ClickdateAnnotationTest)))
    return suite
    



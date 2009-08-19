# -*- coding: UTF-8 -*-
# Dr. Hendrik Bunke, hendrik.bunke@ifw-kiel.de
# Version 0.1 05/2009

# methods for analyzing/viewing dates of downloads, e.g. 'clicks'

from zope.interface import Interface
from Products.Five.browser import BrowserView
from Products.CMFCore.utils import getToolByName
from zope.app.annotation.interfaces import IAnnotations

#from Products.AdvancedQuery import In, Eq, And, Or, Between

#test
#from plone.memoize.instance import memoize

#from hbxt.clickdates.interfaces import IClickdates
import datetime

# TODO 2009-05-07
#   -   Die Downloadzahlen für den letzten Monat sollten irgendwie in den
#       Katalog gespeichert werden.
#   
#   -   !!!Ließe sich evtl. die jeweilige Monatsliste dauerhaft bzw. für
#       den jeweils aktuellen Monat speichern?! Es ist ziemlicher
#       Unsinn, das bei *jedem* Aufruf der Startseite neu zu berechnen,
#       wenn der Stand den ganzen Monat der selbe ist!!!
#       ==> erste Überlegungen:
#            -   Einführung eines OOBTree-Objekts (könnte evtl. auch ein
#                Folder sein), das die Monate (Key)
#                sowie die (sortierten) Dokumente mit Downloadzahlen für
#                den Monat enthält. Das hätte den Vorteil, dass diese
#                Listen auch später noch jederzeit abrufbar wären!
#                Problem dabei: Erreichbar via Navigation?!

ANNOTATION = "hbxt.clickdates"

class IClickdatesView(Interface):
    """
    methods for analyzing/viewing dates of downloads
    """
    
    
    def lastMonth():
        """downloads last month
        """

    def keyLastMonth():
        """generates annotations key for last month.  
        eigene Methode um gegebenfalls (spaeter) die Keygenerierung von der
        template aus aufrufen zu können
        """

    def keyThisMonth():
        """generates annotations key for this month
        """

    def verboseLastMonth():
        """returns Date as Month Year (e.g. July 2009)
        """

    def verboseThisMonth():
        """returns Date of this month as Month Year (e.g. July 2009)
        """

    def thisMonth():
        """downloads count thisMonth
        """

    def sumLastMonth():
        """sums all downloads last month
        """

    def sumThisMonth():
        """sums all downloads this month
        """


class ClickdatesView(BrowserView):
    """
    """
        
 #   @memoize
    def lastMonth(self):
        """
        """
       
        #testing
        #k = "2009-5"
        k = self.keyLastMonth()

        articles = self._getClickdatesObjects()

        result = []
        for article in articles:
            annotations = IAnnotations(article)
            clickdates = annotations[ANNOTATION]
            
            if clickdates.has_key(k):
                clicks = self._countClickdates(article, k)

                #tuple
                result.append((article, clicks))
            
        #Sortierung
        list = sorted(result, key=lambda x:(x[1], x[0]))
        list.reverse()
        
        return list

    
    def sumLastMonth(self):
        """
        """
        s = self.lastMonth()
        sum = 0
        for article in s:
            sum += article[1]

        return sum

    
    def thisMonth(self):
        """
        """
        k = self.keyThisMonth()

        articles = self._getClickdatesObjects()
        result = []
        for article in articles:
            annotations = IAnnotations(article)
            clickdates = annotations[ANNOTATION]
            
            if clickdates.has_key(k):
                clicks = self._countClickdates(article, k)

                #tuple
                result.append((article, clicks))
            
        #Sortierung
        list = sorted(result, key=lambda x:(x[1], x[0]))
        list.reverse()
        
        return list
 
    def sumThisMonth(self):
        """
        """
        s = self.thisMonth()
        sum = 0
        for article in s:
            sum += article[1]

        return sum


  #  @memoize
    def keyLastMonth(self):
        """
        """
        thisMonth = datetime.date.today().month
        thisYear = datetime.date.today().year
    
        if thisMonth == 1:
            lastMonth = 12
            lastMonthYear = thisYear -1
        else:
            lastMonth = thisMonth -1
            lastMonthYear = thisYear

        key = "%s-%s" %(lastMonthYear, lastMonth)
        return key

    
   # @memoize
    def keyThisMonth(self):
        """        
        """
        thisMonth = datetime.date.today().month
        thisYear = datetime.date.today().year
        key = "%s-%s" %(thisYear, thisMonth)
        
        return key


    def _getClickdatesObjects(self):
        """returns all objects with clickdates annotation
        """
        catalog = getToolByName(self.context, "portal_catalog")
        
        # beware: index 'object_provides' is not available in Plone 2.1 and 2.5!
        # Please provide the index by hand or programmatically. You can
        # use the code from Plone 3.x (CatalogTool) 
        brains = catalog.searchResults(object_provides="hbxt.clickdates.interfaces.IClickdatesAnnotatable")

        result = []
        for brain in brains:
            obj = brain.getObject() # optimize! clickdates sollten in irgendeiner Form in den catalog.
            annotations = IAnnotations(obj)
            if annotations.has_key(ANNOTATION):
                result.append(obj)

        return result

    
    def _countClickdates(self, obj, key):
        """count clickdates values in a (by the other classmethods) given list
        """
        annotations = IAnnotations(obj)
        clickdates = annotations[ANNOTATION]
        c = clickdates[key]
        return len(c)

    
    #@memoize
    def verboseLastMonth(self):
        """
        """
        thisMonth = datetime.date.today().month
        thisYear = datetime.date.today().year

        date = datetime.date.today()
    
        if thisMonth == 1:
            lastMonth = 12
            lastMonthYear = thisYear -1
        else:
            lastMonth = thisMonth -1
            lastMonthYear = thisYear

        dateLastMonth = date.replace(month=lastMonth, year=lastMonthYear)
        
        literal = dateLastMonth.strftime("%b %Y")

        return literal


#    @memoize
    def verboseThisMonth(self):
        """
        """
        return datetime.date.today().strftime("%b %Y")

    

        


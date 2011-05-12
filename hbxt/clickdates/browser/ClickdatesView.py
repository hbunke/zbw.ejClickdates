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

    def keyLastMonth(month):
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

    def lastThreeMonth():
        """sums all downloads for the last three months
        """

    def verboseLastThreeMonth():
        """
        returns string for last three month, e.g. Jul - Sep 2009
        """



class ClickdatesView(BrowserView):
    """
    """
        
    def _intLastMonth(self, month):
        """
        returns number of last Month and Year before month
        """
        thisYear = datetime.date.today().year
        if month == 1:
            lastMonth = 12
            lastMonthYear = thisYear -1
        else:
            lastMonth = month -1
            lastMonthYear = thisYear

        return (lastMonthYear, lastMonth)

    def keyLastMonth(self, month):
        """
        """
        lastMonthYear = month[0]
        lastMonth = month[1]
        key = "%s-%s" %(lastMonthYear, lastMonth)
        return key

    
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
        brains = catalog.searchResults(portal_type="JournalPaper", 
                object_provides="hbxt.clickdates.interfaces.IClickdatesAnnotatable")

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


    
    def lastMonth(self):
        """
        """
        
        thisMonth = datetime.date.today().month
        lastMonth = self._intLastMonth(thisMonth)
        k = self.keyLastMonth(lastMonth)


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

    def verboseLastThreeMonth(self):
        """
        """
        date = datetime.date.today()
        thisMonth = datetime.date.today().month
        month1 = self._intLastMonth(thisMonth)
        month2 = self._intLastMonth(month1[1])
        month3 = self._intLastMonth(month2[1])

        date1 = date.replace(month=month3[1], year=month3[0], day=1)
        date2 = date.replace(month=month1[1], year=month1[0], day=1)

        m1 = date1.strftime("%b")
        y1 = date1.strftime("%Y")

        m2 = date2.strftime("%b")
        y2 = date2.strftime("%Y")
        
        if y1 == y2:
            result = "%s - %s %s" %(m1, m2, y1)

        else:
            result = "%s %s - %s %s" %(m1, y1, m2, y2)
        
        return result


    def verboseThisMonth(self):
        """
        """
        return datetime.date.today().strftime("%b %Y")

    
    def lastThreeMonth(self):
        """
        """
        thisMonth = datetime.date.today().month
        month1 = self._intLastMonth(thisMonth)
        month2 = self._intLastMonth(month1[1])
        month3 = self._intLastMonth(month2[1])

        threeMonth = [month1, month2, month3]
        threeMonthKeys = [self.keyLastMonth(month) for month in threeMonth]
        
        articles = self._getClickdatesObjects()

        result = []
        for article in articles:
            annotations = IAnnotations(article)
            clickdates = annotations[ANNOTATION]
            clicks = 0
            
            for key in threeMonthKeys:
                if clickdates.has_key(key):
                    t = self._countClickdates(article, key)
                    clicks += t
            #tuple
            result.append((article, clicks))
            
        #Sortierung
        list = sorted(result, key=lambda x:(x[1], x[0]))
        
        list.reverse()
        
        return list


       
        


# -*- coding: UTF-8 -*-
# Dr. Hendrik Bunke <hendrik.bunke@ifw-kiel.de>

from zope.interface import implements, Interface
from zope.component import adapts
from zope.app.annotation.interfaces import IAnnotations

from hbxt.clickdates.interfaces import IClickdates

from BTrees.OOBTree import OOBTree
from persistent.list import PersistentList

import datetime

KEY = "hbxt.clickdates"

class Clickdates:
    implements(IClickdates)
    adapts(Interface)

    def __init__(self, context):
        
        self.context = context
        annotations =  IAnnotations(context)

        if not annotations.has_key(KEY):
            annotations[KEY] = OOBTree()

        self.dates = annotations[KEY]
        
        # keys werden gebildet aus yyyy-mm, also zb 2009-4

        # zur Auswertung kann dann sowohl ueber die Keys (=einzelne
        # Monate) als auch ueber die values als ganzes (also zb. fuer
        # andere auswertungen wie: tageszeit etc.) iteriert werden
    
    def clickDate(self):
        """adds datetime object as annotation
        """

        thisMonth = datetime.date.today().month
        thisYear = datetime.date.today().year
        k = "%s-%s" %(thisYear, thisMonth)
        t = self.dates
        date = datetime.datetime.now()

        # TODO hier noch Fehlerroutinen einbauen!
        if not t.has_key(k):
            datesList = PersistentList()
            datesList.append(date)
            t.insert(k, datesList)
        else:
            t[k].append(date)
        
        
        


# -*- coding: UTF-8 -*-
# Dr. Hendrik Bunke <hendrik.bunke@ifw-kiel.de>

from zope.interface import Interface
from zope.annotation.interfaces import IAttributeAnnotatable

class IClickdatesAnnotatable(IAttributeAnnotatable):
    """
    Marker Interface
    """

class IClickdates(Interface):
    """
    Interface for storing date of clickevents
    """

    def clickDate(self):
        """
        stores date as annotation
        """
    


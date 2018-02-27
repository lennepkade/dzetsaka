# -*- coding: utf-8 -*-

"""
/***************************************************************************
 className
                                 A QGIS plugin
 desc
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2018-02-24
        copyright            : (C) 2018 by Nicolas Karasiak
        email                : karasiak.nicolas@gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""

__author__ = 'Nicolas Karasiak'
__date__ = '2018-02-24'
__copyright__ = '(C) 2018 by Nicolas Karasiak'

# This will get replaced with a git SHA1 when you do a git archive

__revision__ = '$Format:%H$'
from qgis.PyQt.QtGui import QIcon
import os
from qgis.core import QgsProcessingProvider
#from .moduleName_algorithm import classNameAlgorithm
#from .processing.moduleName_algorithm import classNameAlgorithm
from .processing.medianFilter import medianFilterAlgorithm
from .processing.train import trainAlgorithm
from .processing.classify import classifyAlgorithm
from .processing.splitTrainValidation import splitTrain
from processing.core.ProcessingConfig import ProcessingConfig, Setting
pluginPath = os.path.dirname(__file__)
from qgis.core import QgsMessageLog
"""
import sys
sys.setrecursionlimit(10000) # 10000 is an example, try with different values
"""

class dzetsakaProvider(QgsProcessingProvider):

    def __init__(self):
        QgsProcessingProvider.__init__(self)
    
        # Load algorithms
        self.alglist = [medianFilterAlgorithm(),trainAlgorithm(),classifyAlgorithm(),splitTrain()]
    
    def icon(self):
        """
        add icon
        """
        iconPath = os.path.join(pluginPath,'img','icon.png')
     
        return QIcon(os.path.join(iconPath))
    
    def unload(self):
        """
        Unloads the provider. Any tear-down steps required by the provider
        should be implemented here.
        """
        pass
        
    def loadAlgorithms(self):
        """
        Loads all algorithms belonging to this provider.
        """
        
        for alg in self.alglist:
            self.addAlgorithm( alg )
    
    def id(self):
        """
        Returns the unique provider id, used for identifying the provider. This
        string should be a unique, short, character only string, eg "qgis" or
        "gdal". This string should not be localised.
        """
        return 'dzetsaka'

    def name(self):
        """
        Returns the provider name, which is used to describe the provider
        within the GUI.

        This string should be short (e.g. "Lastools") and localised.
        """
        return self.tr('dzetsaka')

    def longName(self):
        """
        Returns the a longer version of the provider name, which can include
        extra details such as version numbers. E.g. "Lastools LIDAR tools
        (version 2.2.1)". This string should be localised. The default
        implementation returns the same string as name().
        """
        return self.name()

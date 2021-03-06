# -*- coding: utf-8 -*-

"""
/***************************************************************************
 className
                                 A QGIS plugin
 description
                              -------------------
        begin                : 2016-12-03
        copyright            : (C) 2016 by Nico
        email                : nico@nico
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


# from ... import dzetsaka.scripts.function_dataraster as dataraster

#from PyQt4.QtGui import QIcon
#from PyQt4.QtCore import QSettings


from qgis.PyQt.QtGui import QIcon
from PyQt5.QtCore import QCoreApplication

from qgis.core import (QgsMessageLog,
                       QgsProcessingAlgorithm,
                       QgsProcessingParameterRasterLayer,
                       QgsProcessingParameterNumber,
                       QgsProcessingParameterRasterDestination,
                       QgsRasterLayer)
import os
try:
    from osgeo import gdal
except ImportError:
    import gdal
from ..scripts import function_dataraster as dataraster
import numpy as np
import math

pluginPath = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        os.pardir))
# EX
"""
from processing.core.GeoAlgorithm import GeoAlgorithm
from processing.core.parameters import ParameterRaster
from processing.core.parameters import ParameterNumber
from processing.core.outputs import OutputRaster
"""


class shannonAlgorithm(QgsProcessingAlgorithm):
    """This is an example algorithm that takes a vector layer and
    creates a new one just with just those features of the input
    layer that are selected.

    It is meant to be used as an example of how to create your own
    algorithms and explain methods and variables used to do it. An
    algorithm like this will be available in all elements, and there
    is not need for additional work.

    All Processing algorithms should extend the GeoAlgorithm class.
    """

    # Constants used to refer to parameters and outputs. They will be
    # used when calling the algorithm from another algorithm, or when
    # calling from the QGIS console.

    INPUT_RASTER = 'INPUT_RASTER'
    OUTPUT_RASTER = 'OUTPUT_RASTER'

    def icon(self):

        return QIcon(os.path.join(pluginPath, 'icon.png'))

    def initAlgorithm(self, config=None):
        """Here we define the inputs and output of the algorithm, along
        with some other properties.
        """

        # We add the input vector layer. It can have any kind of geometry
        # It is a mandatory (not optional) one, hence the False argument
        self.addParameter(
            QgsProcessingParameterRasterLayer(
                self.INPUT_RASTER,
                self.tr('Input raster')
            )
        )

        # We add a raster as output
        self.addParameter(
            QgsProcessingParameterRasterDestination(
                self.OUTPUT_RASTER,
                self.tr('Output raster')
            )
        )
        # add num

    def name(self):
        """
        Returns the algorithm name, used for identifying the algorithm. This
        string should be fixed for the algorithm, and must not be localised.
        The name should be unique within each provider. Names should contain
        lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Shannon entropy'

    def processAlgorithm(self, parameters, context, feedback):
        """Here is where the processing itself takes place."""

        INPUT_RASTER = self.parameterAsRasterLayer(
            parameters, self.INPUT_RASTER, context)
        #INPUT_RASTER = self.getParameterValue(self.INPUT_RASTER)
        OUTPUT_RASTER = self.parameterAsOutputLayer(
            parameters, self.OUTPUT_RASTER, context)

        """
        MEDIAN_ITER = self.parameterAsInt(parameters, self.MEDIAN_ITER, context)
        MEDIAN_SIZE = self.parameterAsInt(parameters, self.MEDIAN_SIZE, context)
        # First we create the output layer. The output value entered by
        # the user is a string containing a filename, so we can use it
        # directly

        #from scipy import ndimage
        #import gdal
        """
        INPUT_RASTER_src = INPUT_RASTER.source()

        # feedback.pushInfo(str(OUTPUT_RASTER))
        #QgsMessageLog.logMessage('output is: '+str(OUTPUT_RASTER))

        # on importe l'image
        im = openRaster(INPUT_RASTER_src)
        # on crée notre image à 6 bandes
        im2 = calcul_shannon(im)

        # data pour l'écriture
        data = gdal.Open(INPUT_RASTER_src)
        GeoTransform = data.GetGeoTransform()
        Projection = data.GetProjection()

        # on l'enregistre

        saveRaster(OUTPUT_RASTER, im2, GeoTransform, Projection)

        return {self.OUTPUT_RASTER: OUTPUT_RASTER}

        # return OUTPUT_RASTER

    def tr(self, string):
        return QCoreApplication.translate('Processing', string)

    def createInstance(self):
        return shannonAlgorithm()

    def displayName(self):
        """
        Returns the translated algorithm name, which should be used for any
        user-visible display of the algorithm name.
        """
        return self.tr(self.name())

    def group(self):
        """
        Returns the name of the group this algorithm belongs to. This string
        should be localised.
        """
        return self.tr(self.groupId())

    def groupId(self):
        """
        Returns the unique ID of the group this algorithm belongs to. This
        string should be fixed for the algorithm, and must not be localised.
        The group id should be unique within each provider. Group id should
        contain lowercase alphanumeric characters only and no spaces or other
        formatting characters.
        """
        return 'Raster tool'


def calcul_shannon(image):
    """
    The function will set all the first three bands, corresponding to the fractions, to sum unity.
    INPUT image : Image tableau scipy à 13bandes
    OUTPUT resultat : Image tableau scipy à 6 bandes avec
        bande 1: première valeur maximale max1
        bande 2: deuxième valeur maximale max2
        bande 3: troisième valeur maximale max3
        bande 4: catégorie (espèce) correspondante à la valeur max1
        bande 5: catégorie (espèce) correspondante à la valeur max2
        bande 6: catégorie (espèce) correspondante à la valeur max3
    """
    # on recupère les dimensions de notre image : (4036, 4531, 13)
    shape = np.shape(image)
    # on cree notre tableau pour stocker la sortie
    outputShape = (shape[0], shape[1], 1)
    dimX = outputShape[0]
    dimY = outputShape[1]
    nbBandes = shape[2]
    resultat = np.zeros(outputShape)

    # boucle pour retrouver chaque pixel:
    for i in range(0, dimX):
        for j in range(0, dimY):
            # on est dans un pixel de coordonnees (i,j), array taille 13:
            # image[i,j,:]

            shannon = float(0)

            for k in range(0, nbBandes):  # de 0 à 13
                if(image[i, j, k] != 0):  # on stocke max_i
                    shannon = shannon + image[i, j,
                                              k] * math.log(image[i, j, k], 2)

            resultat[i, j, 0] = -shannon

    return resultat


def openRaster(filepath):
    """
    The function is an adaptation of the rasterTool.py provided
    It opens the raster located in the given input
    INPUT filepath : adress of the .tiff file à traiter
    OUTPUT im : Image tableau scipy contenant les 13 bandes de l'image
    """
    # Open the file:
    data = gdal.Open(filepath)
    nc = data.RasterXSize
    nl = data.RasterYSize
    d = data.RasterCount

    # chech dataType
    gdal_dt = data.GetRasterBand(1).DataType

    # on met dans un tableau nos 13 bandes
    print(type(data))

    im = np.empty((nl, nc, d), dtype=np.float32)
    for i in range(d):
        im[:, :, i] = data.GetRasterBand(i + 1).ReadAsArray()

    # Close the file
    data = None
    # On retourne l'image résultante
    return im


def saveRaster(nomSortie, image, GeoTransform, Projection):
    """
    The function saves the resultant image in the hard disk. Adaptation de write_data sous rasterTool.py
    INPUT   image : tableau recalculé à 6 bandes.
            GeoTransform,Projection : informations from original image
    """
    nl, nc, d = np.shape(image)
    # ou image.shape; ?

    # we create an empty image in GeoTiff
    driver = gdal.GetDriverByName('GTiff')

    dt = image.dtype.name
    if(dt == 'float64'):
        gdal_dt = gdal.GDT_Float64
    else:
        print("Erreur de type de données")
        print(dt)
        exit()

    # blehbleh . "on récupére l'image dans le tableau outname avec ses différents bandes et
    # les métadonnées et la projection données en paramétre de la fonction"
    dst_ds = driver.Create(nomSortie, nc, nl, d, gdal_dt)
    dst_ds.SetGeoTransform(GeoTransform)
    dst_ds.SetProjection(Projection)

    for i in range(d):
        out = dst_ds.GetRasterBand(i + 1)
        # on affecte l'image dans le fichier enregistré
        out.WriteArray(image[:, :, i])
        out.FlushCache()

    dst_ds = None

# -*- coding: utf-8 -*-
"""
/***************************************************************************
 DimLao
                                 A QGIS plugin
 DimLao
                             -------------------
        begin                : 2014-08-05
        copyright            : (C) 2014 by Stefan Ziegler
        email                : edi.gonzales@gmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    from .dimlao import DimLao
    return DimLao(iface)

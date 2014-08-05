# -*- coding: utf-8 -*-
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

import time, os, math

class CreateDimensions(QObject):
    def __init__(self, iface, outputdir, layer, ident, scale, selectedfeatures):
        self.iface = iface
        self.myOutputDir = outputdir
        self.myLayer = layer
        self.myIdent = ident
        self.myScale = scale
        self.mySelectedFeatures = selectedfeatures

        
    def run(self):
        # create line vector layer with dimensions (=boundary)
        crs = self.iface.mapCanvas().mapSettings().destinationCrs().authid()
        
        fields = "&field=parcelnr:string(200)"
        fields += "&field=len_txt:string(50)"
        
        layer_title = "dimensions"
        
        boundarylayer = QgsVectorLayer("LineString?crs=" + crs + fields+ "&index=yes", layer_title, "memory")
        self.boundaryprovider = boundarylayer.dataProvider()
        
        
        # create boundary points layer
        fields = "&field=parcelnr:string(200)"
        
        layer_title = "boundarypoints"
        
        pointlayer = QgsVectorLayer("Point?crs=" + crs + fields+ "&index=yes", layer_title, "memory")
        self.pointprovider = pointlayer.dataProvider()
        
        # loop through features for dimensions and boundary points
        vlayer = self.getVectorLayerByName(self.myLayer)
        
        if vlayer == None:
            QMessageBox.critical(None, "DimLao", QCoreApplication.translate("DimLao", "Layer not found."))            
            return        

        if self.mySelectedFeatures == True:
            featids = vlayer.selectedFeaturesIds()
            if len(featids) == 0:
                return
            iter = vlayer.selectedFeatures()
        else:
            iter = vlayer.getFeatures()

        pidIndex = vlayer.fieldNameIndex(self.myIdent)
        
        for feature in iter:
            geom = feature.geometry()
            pid = feature.attributes()[pidIndex]

            wkbtype=geom.wkbType()

            if wkbtype in [QGis.WKBPolygon,QGis.WKBPolygon25D]:
                for line in geom.asPolygon():
                    self.splitline(line, pid)

            if wkbtype in [QGis.WKBMultiPolygon,QGis.WKBMultiPolygon25D]:
                for poly in geom.asMultiPolygon():
                    for line in poly:
                        self.splitline(line, pid)                        

        boundarylayer.updateExtents()      
        pointlayer.updateExtents()      

        # write dimensions memory layer to shape file
        # use crs of project
        myTime = QDateTime.currentDateTime()        
        timeSuffix = str(myTime.toString(Qt.ISODate)).replace(":", "").replace("-", "")
        
        fileName = QDir.convertSeparators(QDir.cleanPath(self.myOutputDir + os.sep + "dimensions" + timeSuffix + ".shp"))
        error = QgsVectorFileWriter.writeAsVectorFormat(boundarylayer, fileName, "utf-8", self.iface.mapCanvas().mapSettings().destinationCrs(), "ESRI Shapefile")
        if error == QgsVectorFileWriter.NoError:
            self.iface.messageBar().pushMessage("Information", QCoreApplication.translate("DimLao", "Boundary lines layer written."), level=QgsMessageBar.INFO, duration=3)
        else:
            self.iface.messageBar().pushMessage("Error", QCoreApplication.translate("DimLao", "Error writing: ") + filename, level=QgsMessageBar.CRITICAL, duration=5)            
            return
            
        # write boundary points
        fileName = QDir.convertSeparators(QDir.cleanPath(self.myOutputDir + os.sep + "boundarypoints" + timeSuffix + ".shp"))
        error = QgsVectorFileWriter.writeAsVectorFormat(pointlayer, fileName, "utf-8", self.iface.mapCanvas().mapSettings().destinationCrs(), "ESRI Shapefile")
        if error == QgsVectorFileWriter.NoError:
            self.iface.messageBar().pushMessage("Information", QCoreApplication.translate("DimLao", "Boundary points layer written."), level=QgsMessageBar.INFO, duration=3)            
        else:
            self.iface.messageBar().pushMessage("Error", QCoreApplication.translate("DimLao", "Error writing: ") + filename, level=QgsMessageBar.CRITICAL, duration=5)            
            return
            
        # create the short lines of the adjacent parcels        
        fields = "&field=parcelnr:string(200)"
        
        layer_title = "boundarysnippets"
        
        neighborlayer = QgsVectorLayer("LineString?crs=" + crs + fields+ "&index=yes", layer_title, "memory")
        self.neighborlayer = neighborlayer.dataProvider()
        
        ##### BIS HIERHER
        
        # create spatial index
        pr = vlayer.dataProvider()
        fe = QgsFeature()
        allAttrs = pr.attributeIndexes()
        pr.select(allAttrs)
        
        index = QgsSpatialIndex()        
        while pr.nextFeature(fe):
            index.insertFeature(fe)
            
#        print "spatialindex erzeugt"
            
        # and now process the snippets
        for fid in featids:
            feat = QgsFeature()
            vlayer.featureAtId(fid, feat)
            pid = feat.attributeMap()[pidIndex].toString()
#            print "fid: " + str(fid)
#            print "pid: " + str(pid)

            geom =  feat.geometry()
            bbox = geom.boundingBox()

            if self.myScale == "500":
                print "500"
                bufferDistance = 4*500 / 1000
            elif self.myScale == "1000":
                print "1000"
                bufferDistance = 2*1000 / 1000
            else:
                bufferDistance = 2
                
            bufferGeom = geom.buffer(bufferDistance, 8)
           
           
            intersect = index.intersects(bbox)
#            print "intersects liste"
#            print intersect
            for i in intersect:
#                print str(i)
                f = QgsFeature()
                vlayer.featureAtId(i, f)
                g = f.geometry()
                if geom.touches(g):
                    if i <> fid:
#                        print "touches" + str(i)
                        # Umwandlung des Polygons in einen LineString. Input MUSS Polygon sein und nicht MulitPolygon!!
                        intersection = bufferGeom.intersection(QgsGeometry.fromPolyline(g.asPolygon()[0]))
#                        print intersection.exportToWkt()
            
                        wkbtype = intersection.wkbType()
#                        print "wkbtype"
#                        print wkbtype
                        if wkbtype in [QGis.WKBLineString,QGis.WKBLineString25D]:
#                            print "linestring"
                            fet = QgsFeature()
                            fet.setGeometry( intersection )
                            fet.setAttributeMap( {0 : QVariant(pid)} )
                            self.neighborprovider.addFeatures( [ fet ] )

                        if wkbtype in [QGis.WKBMultiLineString,QGis.WKBMultiLineString25D]:
#                            print "multilinestring"
                            for line in intersection.asMultiPolyline():
#                                print "line"
#                                print line
                                fet = QgsFeature()
                                fet.setGeometry( QgsGeometry.fromPolyline(line) )
                                fet.setAttributeMap( {0 : QVariant(pid)} )
                                self.neighborprovider.addFeatures( [ fet ] )
                    
        neighborlayer.updateExtents()      

        # write adjacent polygons snippets
        fileName = QDir.convertSeparators(QDir.cleanPath(self.myOutputDir + os.sep + "adjacent" + timeSuffix + ".shp"))
        error = QgsVectorFileWriter.writeAsVectorFormat(neighborlayer, fileName, "utf-8", None, "ESRI Shapefile")
        if error == QgsVectorFileWriter.NoError:
          print "success!"
        else:
            QMessageBox.critical(None, "DimLao", QCoreApplication.translate("DimLao", "Error writing: " + filename))            
            return


    def splitline(self, line, pid):
        for i in range(1, len(line)):
            myLine = line[i-1:i+1]
            p1 = myLine[0]
            p2 = myLine[1]
            
            newline = QgsGeometry.fromPolyline([p1, p2])
            
            dist = newline.length()
            myLength = str(round(float(dist), 1)) + "0"
            
            fet = QgsFeature()
            fet.setGeometry( newline )
            fet.setAttributes([pid, myLength])
            self.boundaryprovider.addFeatures( [ fet ] )
            
            newpoint = QgsGeometry.fromPoint(QgsPoint(p1))
            fet = QgsFeature()
            fet.setGeometry( newpoint )
            fet.setAttributes([pid])
            self.pointprovider.addFeatures( [ fet ] )


    # Return QgsVectorLayer from a layer name ( as string )
    # (c) Carson Farmer / fTools
    def getVectorLayerByName(self, myName):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in layermap.iteritems():
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == myName:
                if layer.isValid():
                    return layer
                else:
                    return None    

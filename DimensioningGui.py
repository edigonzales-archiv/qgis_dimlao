# -*- coding: utf-8 -*-

# Import the PyQt and the QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *

import locale

from Ui_dimensioning import Ui_Dimensioning

class DimensioningGui(QDialog, Ui_Dimensioning):
  
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        
        self.okButton = self.buttonBox.button(QDialogButtonBox.Ok)        
        self.connect(self.okButton, SIGNAL("accepted()"), self.accept)
        
        # get the settings
        self.settings = QSettings("CatAIS","DimLao")
        self.outputdirpath = self.settings.value("outputdirpath")


    def initGui(self):       
        self.lineEditOutputDir.setText(self.settings.value("outputdirpath")) 

        self.cBoxOutputScale.clear()
        self.cBoxOutputScale.insertItem(1, str("1:500"), int(500))
        self.cBoxOutputScale.insertItem(2, str("1:1000"), int(1000))
        self.cBoxOutputScale.insertItem(3, str("1:2000"), int(2000))
        self.cBoxOutputScale.insertItem(4, str("1:4000"), int(4000))

        layers = self.getLayerNames([2])
        self.cBoxParcelLayer.clear()
        for layer in layers:
            self.cBoxParcelLayer.insertItem(self.cBoxParcelLayer.count(), unicode(layer), str(unicode(layer)))
        
        
    @pyqtSignature("on_btnBrowseOutputDir_clicked()")    
    def on_btnBrowseOutputDir_clicked(self):
        dir = QFileDialog.getExistingDirectory(self, QCoreApplication.translate("DimLao", "Choose output directory"), self.outputdirpath)
        dirInfo = QFileInfo(dir)
        self.lineEditOutputDir.setText(str(dirInfo.absoluteFilePath()))


    @pyqtSignature("on_cBoxParcelLayer_currentIndexChanged(QString)")      
    def on_cBoxParcelLayer_currentIndexChanged(self):    
        vlayer = self.getVectorLayerByName(self.cBoxParcelLayer.currentText())

        if vlayer == None:
            return

        provider = vlayer.dataProvider()
        fields = provider.fields()
        
        self.cBoxParcelNumberIdent.clear()
        for field in fields:
            self.cBoxParcelNumberIdent.insertItem(self.cBoxParcelNumberIdent.count(), field.name())


        
    def accept(self):
        self.settings.setValue("outputdirpath", self.lineEditOutputDir.text())

        myOutputDir = self.lineEditOutputDir.text()
        myLayer = self.cBoxParcelLayer.currentText()
        myParcelIdent = self.cBoxParcelNumberIdent.currentText()
        myScale = self.cBoxOutputScale.itemData(self.cBoxOutputScale.currentIndex())
        mySelectedFeatures = self.checkBoxSelectedOnly.isChecked()

        if myOutputDir == "":
            QMessageBox.warning(None, "DimLao", QCoreApplication.translate("DimLao", "No output directory set."))
            return
            
        if myLayer == "":
            QMessageBox.warning(None, "DimLao", QCoreApplication.translate("DimLao", "No parcel layer chosen."))
            return            
            
        if myParcelIdent == "":
            QMessageBox.warning(None, "DimLao", QCoreApplication.translate("DimLao", "No parcel number identifaction chosen."))
            return                        
        
        self.emit( SIGNAL("okClickedDimensioning(QString, QString, QString, QString, bool)"), myOutputDir, myLayer, myParcelIdent, str(myScale), mySelectedFeatures)


    # Return list of names of all layers in QgsMapLayerRegistry
    # (c) Carson Farmer / fTools
    def getLayerNames(self, vTypes):
        layermap = QgsMapLayerRegistry.instance().mapLayers()
        layerlist = []
        if vTypes == "all":
            for name, layer in layermap.iteritems():
                layerlist.append(unicode( layer.name()))
        else:
            for name, layer in layermap.iteritems():
                if layer.type() == QgsMapLayer.VectorLayer:
                    if layer.geometryType() in vTypes:
                        layerlist.append(unicode(layer.name()))
                elif layer.type() == QgsMapLayer.RasterLayer:
                    if "Raster" in vTypes:
                        layerlist.append(unicode(layer.name()))
        return sorted(layerlist, cmp=locale.strcoll)
            

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
            

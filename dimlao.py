from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

import sys, os, time
import resources

class DimLao:

    def __init__(self, iface):
        self.iface = iface
        self.canvas = self.iface.mapCanvas()
        
    
    def initGui(self):
        self.action_dimensioning= QAction(QIcon(":/plugins/dimlao/icons/dimensioning.png"),  "Calculate dimensioning",  self.iface.mainWindow())        
        QObject.connect(self.action_dimensioning,  SIGNAL("triggered()"),  self.showDialog) 
        
        self.iface.addPluginToMenu(self.action_dimensioning.tr("DimLao"), self.action_dimensioning)        
        self.iface.addToolBarIcon(self.action_dimensioning)
        
    
    def showDialog(self):
        from DimensioningGui import DimensioningGui
        self.ctrl = DimensioningGui(self.iface.mainWindow())
        self.ctrl.initGui()
        self.ctrl.show()
        
        QObject.connect(self.ctrl, SIGNAL("okClickedDimensioning(QString, QString, QString, QString, bool)"), self.calculateDimensioning)


    def calculateDimensioning(self, myOutputDir, myLayer, myParcelIdent, myScale, mySelectedFeatures):
        from CreateDimensions import CreateDimensions
        d = CreateDimensions(self.iface, myOutputDir, myLayer, myParcelIdent, myScale, mySelectedFeatures)
        d.run()
    


    def unload(self):
        self.iface.removePluginMenu(self.action_dimensioning.tr("Dimensioning"), self.action_dimensioning)        
        self.iface.removeToolBarIcon(self.action_dimensioning)

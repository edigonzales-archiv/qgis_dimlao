# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'Ui_dimensioning.ui'
#
# Created: Tue Aug  5 19:32:25 2014
#      by: PyQt4 UI code generator 4.9.1
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Dimensioning(object):
    def setupUi(self, Dimensioning):
        Dimensioning.setObjectName(_fromUtf8("Dimensioning"))
        Dimensioning.resize(493, 298)
        self.gridLayout_3 = QtGui.QGridLayout(Dimensioning)
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.groupBox = QtGui.QGroupBox(Dimensioning)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.gridLayout_2 = QtGui.QGridLayout(self.groupBox)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.lineEditOutputDir = QtGui.QLineEdit(self.groupBox)
        self.lineEditOutputDir.setObjectName(_fromUtf8("lineEditOutputDir"))
        self.gridLayout.addWidget(self.lineEditOutputDir, 0, 1, 1, 1)
        self.label = QtGui.QLabel(self.groupBox)
        self.label.setMinimumSize(QtCore.QSize(0, 27))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.btnBrowseOutputDir = QtGui.QPushButton(self.groupBox)
        self.btnBrowseOutputDir.setObjectName(_fromUtf8("btnBrowseOutputDir"))
        self.gridLayout.addWidget(self.btnBrowseOutputDir, 0, 2, 1, 1)
        self.cBoxParcelLayer = QtGui.QComboBox(self.groupBox)
        self.cBoxParcelLayer.setObjectName(_fromUtf8("cBoxParcelLayer"))
        self.gridLayout.addWidget(self.cBoxParcelLayer, 1, 1, 1, 1)
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setMinimumSize(QtCore.QSize(0, 27))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 0, 1, 1)
        self.cBoxOutputScale = QtGui.QComboBox(self.groupBox)
        self.cBoxOutputScale.setEnabled(True)
        self.cBoxOutputScale.setMinimumSize(QtCore.QSize(0, 0))
        self.cBoxOutputScale.setObjectName(_fromUtf8("cBoxOutputScale"))
        self.gridLayout.addWidget(self.cBoxOutputScale, 3, 1, 1, 1)
        self.labelAppSubModule = QtGui.QLabel(self.groupBox)
        self.labelAppSubModule.setEnabled(True)
        self.labelAppSubModule.setMinimumSize(QtCore.QSize(0, 27))
        self.labelAppSubModule.setObjectName(_fromUtf8("labelAppSubModule"))
        self.gridLayout.addWidget(self.labelAppSubModule, 3, 0, 1, 1)
        self.checkBoxSelectedOnly = QtGui.QCheckBox(self.groupBox)
        self.checkBoxSelectedOnly.setMinimumSize(QtCore.QSize(0, 23))
        self.checkBoxSelectedOnly.setText(_fromUtf8(""))
        self.checkBoxSelectedOnly.setObjectName(_fromUtf8("checkBoxSelectedOnly"))
        self.gridLayout.addWidget(self.checkBoxSelectedOnly, 4, 1, 1, 1)
        self.label_2 = QtGui.QLabel(self.groupBox)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 4, 0, 1, 1)
        self.cBoxParcelNumberIdent = QtGui.QComboBox(self.groupBox)
        self.cBoxParcelNumberIdent.setObjectName(_fromUtf8("cBoxParcelNumberIdent"))
        self.gridLayout.addWidget(self.cBoxParcelNumberIdent, 2, 1, 1, 1)
        self.label_3 = QtGui.QLabel(self.groupBox)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dimensioning)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout_3.addWidget(self.buttonBox, 1, 0, 1, 1)

        self.retranslateUi(Dimensioning)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dimensioning.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dimensioning.reject)
        QtCore.QMetaObject.connectSlotsByName(Dimensioning)

    def retranslateUi(self, Dimensioning):
        Dimensioning.setWindowTitle(QtGui.QApplication.translate("Dimensioning", "Dimensioning", None, QtGui.QApplication.UnicodeUTF8))
        self.groupBox.setTitle(QtGui.QApplication.translate("Dimensioning", "Dimensioning", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Dimensioning", "Output directory: ", None, QtGui.QApplication.UnicodeUTF8))
        self.btnBrowseOutputDir.setText(QtGui.QApplication.translate("Dimensioning", "Browse", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setText(QtGui.QApplication.translate("Dimensioning", "Parcel layer: ", None, QtGui.QApplication.UnicodeUTF8))
        self.labelAppSubModule.setText(QtGui.QApplication.translate("Dimensioning", "Output scale: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Dimensioning", "Selected features only: ", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Dimensioning", "Parcel number ident: ", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/logement.ui'
#
# Created: Tue May 29 19:14:52 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Logement(object):
    def setupUi(self, Logement):
        Logement.setObjectName(_fromUtf8("Logement"))
        Logement.resize(300, 175)
        Logement.setMinimumSize(QtCore.QSize(300, 175))
        Logement.setMaximumSize(QtCore.QSize(300, 175))
        Logement.setWindowTitle(QtGui.QApplication.translate("Logement", "Logement du ménage", None, QtGui.QApplication.UnicodeUTF8))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        Logement.setWindowIcon(icon)
        self.gridLayout_2 = QtGui.QGridLayout(Logement)
        self.gridLayout_2.setObjectName(_fromUtf8("gridLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Logement)
        self.label.setText(QtGui.QApplication.translate("Logement", "Statut d\'occupation", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.comboSo = QtGui.QComboBox(Logement)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.comboSo.sizePolicy().hasHeightForWidth())
        self.comboSo.setSizePolicy(sizePolicy)
        self.comboSo.setObjectName(_fromUtf8("comboSo"))
        self.comboSo.addItem(_fromUtf8(""))
        self.comboSo.setItemText(0, QtGui.QApplication.translate("Logement", "Propriétaire accédant", None, QtGui.QApplication.UnicodeUTF8))
        self.comboSo.addItem(_fromUtf8(""))
        self.comboSo.setItemText(1, QtGui.QApplication.translate("Logement", "Propriétaire non accédant", None, QtGui.QApplication.UnicodeUTF8))
        self.comboSo.addItem(_fromUtf8(""))
        self.comboSo.setItemText(2, QtGui.QApplication.translate("Logement", "Locataire", None, QtGui.QApplication.UnicodeUTF8))
        self.gridLayout.addWidget(self.comboSo, 0, 1, 1, 2)
        self.label_2 = QtGui.QLabel(Logement)
        self.label_2.setText(QtGui.QApplication.translate("Logement", "Loyer mensuel", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtGui.QLabel(Logement)
        self.label_3.setText(QtGui.QApplication.translate("Logement", "Code postal", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtGui.QLabel(Logement)
        self.label_4.setText(QtGui.QApplication.translate("Logement", "Commune", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.commune = QtGui.QLabel(Logement)
        self.commune.setText(QtGui.QApplication.translate("Logement", "dfe", None, QtGui.QApplication.UnicodeUTF8))
        self.commune.setObjectName(_fromUtf8("commune"))
        self.gridLayout.addWidget(self.commune, 3, 1, 1, 2)
        self.label_6 = QtGui.QLabel(Logement)
        self.label_6.setText(QtGui.QApplication.translate("Logement", "Zone allocation logement", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 4, 0, 1, 1)
        self.spinCP = QtGui.QSpinBox(Logement)
        self.spinCP.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinCP.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinCP.setMaximum(99999)
        self.spinCP.setProperty("value", 69001)
        self.spinCP.setObjectName(_fromUtf8("spinCP"))
        self.gridLayout.addWidget(self.spinCP, 2, 1, 1, 1)
        self.spinZone = QtGui.QSpinBox(Logement)
        self.spinZone.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinZone.setReadOnly(True)
        self.spinZone.setButtonSymbols(QtGui.QAbstractSpinBox.NoButtons)
        self.spinZone.setMinimum(1)
        self.spinZone.setMaximum(3)
        self.spinZone.setProperty("value", 2)
        self.spinZone.setObjectName(_fromUtf8("spinZone"))
        self.gridLayout.addWidget(self.spinZone, 4, 1, 1, 1)
        self.spinLoyer = QtGui.QSpinBox(Logement)
        self.spinLoyer.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.spinLoyer.setMaximum(99999)
        self.spinLoyer.setSingleStep(100)
        self.spinLoyer.setObjectName(_fromUtf8("spinLoyer"))
        self.gridLayout.addWidget(self.spinLoyer, 1, 1, 1, 1)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 2, 1, 1)
        self.gridLayout_2.addLayout(self.gridLayout, 0, 0, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout_2.addItem(spacerItem1, 1, 0, 1, 1)
        self.bbox = QtGui.QDialogButtonBox(Logement)
        self.bbox.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        self.bbox.setOrientation(QtCore.Qt.Horizontal)
        self.bbox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.bbox.setObjectName(_fromUtf8("bbox"))
        self.gridLayout_2.addWidget(self.bbox, 2, 0, 1, 1)

        self.retranslateUi(Logement)
        self.comboSo.setCurrentIndex(2)
        QtCore.QObject.connect(self.bbox, QtCore.SIGNAL(_fromUtf8("accepted()")), Logement.accept)
        QtCore.QObject.connect(self.bbox, QtCore.SIGNAL(_fromUtf8("rejected()")), Logement.reject)
        QtCore.QMetaObject.connectSlotsByName(Logement)

    def retranslateUi(self, Logement):
        pass

import resources_rc

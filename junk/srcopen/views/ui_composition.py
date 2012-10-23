# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui/composition.ui'
#
# Created: Tue May 29 19:14:51 2012
#      by: PyQt4 UI code generator 4.8.5
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    _fromUtf8 = lambda s: s

class Ui_Menage(object):
    def setupUi(self, Menage):
        Menage.setObjectName(_fromUtf8("Menage"))
        Menage.resize(393, 199)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Menage.sizePolicy().hasHeightForWidth())
        Menage.setSizePolicy(sizePolicy)
        Menage.setMinimumSize(QtCore.QSize(393, 181))
        Menage.setToolTip(_fromUtf8(""))
        Menage.setLocale(QtCore.QLocale(QtCore.QLocale.French, QtCore.QLocale.France))
        Menage.setFeatures(QtGui.QDockWidget.AllDockWidgetFeatures)
        Menage.setWindowTitle(QtGui.QApplication.translate("Menage", "Composition du Ménage", None, QtGui.QApplication.UnicodeUTF8))
        self.dockWidgetContents = QtGui.QWidget()
        self.dockWidgetContents.setObjectName(_fromUtf8("dockWidgetContents"))
        self.verticalLayout = QtGui.QVBoxLayout(self.dockWidgetContents)
        self.verticalLayout.setSpacing(3)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(2)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.save_btn = QtGui.QPushButton(self.dockWidgetContents)
        self.save_btn.setToolTip(QtGui.QApplication.translate("Menage", "Enregistrer le cas type", None, QtGui.QApplication.UnicodeUTF8))
        self.save_btn.setText(_fromUtf8(""))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/document-save.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.save_btn.setIcon(icon)
        self.save_btn.setIconSize(QtCore.QSize(22, 22))
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.horizontalLayout.addWidget(self.save_btn)
        self.open_btn = QtGui.QPushButton(self.dockWidgetContents)
        self.open_btn.setToolTip(QtGui.QApplication.translate("Menage", "Ouvrir un cas type", None, QtGui.QApplication.UnicodeUTF8))
        self.open_btn.setText(_fromUtf8(""))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/document-open.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.open_btn.setIcon(icon1)
        self.open_btn.setIconSize(QtCore.QSize(22, 22))
        self.open_btn.setObjectName(_fromUtf8("open_btn"))
        self.horizontalLayout.addWidget(self.open_btn)
        self.line_2 = QtGui.QFrame(self.dockWidgetContents)
        self.line_2.setFrameShape(QtGui.QFrame.VLine)
        self.line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_2.setObjectName(_fromUtf8("line_2"))
        self.horizontalLayout.addWidget(self.line_2)
        self.add_btn = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        self.add_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.add_btn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.add_btn.setToolTip(QtGui.QApplication.translate("Menage", "Ajouter un individu", None, QtGui.QApplication.UnicodeUTF8))
        self.add_btn.setText(_fromUtf8(""))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/list-add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.add_btn.setIcon(icon2)
        self.add_btn.setIconSize(QtCore.QSize(22, 22))
        self.add_btn.setObjectName(_fromUtf8("add_btn"))
        self.horizontalLayout.addWidget(self.add_btn)
        self.rmv_btn = QtGui.QPushButton(self.dockWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.rmv_btn.sizePolicy().hasHeightForWidth())
        self.rmv_btn.setSizePolicy(sizePolicy)
        self.rmv_btn.setMinimumSize(QtCore.QSize(0, 0))
        self.rmv_btn.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.rmv_btn.setToolTip(QtGui.QApplication.translate("Menage", "Retirer un individu", None, QtGui.QApplication.UnicodeUTF8))
        self.rmv_btn.setText(_fromUtf8(""))
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/list-remove.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.rmv_btn.setIcon(icon3)
        self.rmv_btn.setIconSize(QtCore.QSize(22, 22))
        self.rmv_btn.setObjectName(_fromUtf8("rmv_btn"))
        self.horizontalLayout.addWidget(self.rmv_btn)
        self.line_3 = QtGui.QFrame(self.dockWidgetContents)
        self.line_3.setFrameShape(QtGui.QFrame.VLine)
        self.line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.line_3.setObjectName(_fromUtf8("line_3"))
        self.horizontalLayout.addWidget(self.line_3)
        self.lgt_btn = QtGui.QPushButton(self.dockWidgetContents)
        self.lgt_btn.setToolTip(QtGui.QApplication.translate("Menage", "Logement du ménage", None, QtGui.QApplication.UnicodeUTF8))
        self.lgt_btn.setText(_fromUtf8(""))
        icon4 = QtGui.QIcon()
        icon4.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/home.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.lgt_btn.setIcon(icon4)
        self.lgt_btn.setIconSize(QtCore.QSize(22, 22))
        self.lgt_btn.setObjectName(_fromUtf8("lgt_btn"))
        self.horizontalLayout.addWidget(self.lgt_btn)
        self.inf_btn = QtGui.QPushButton(self.dockWidgetContents)
        self.inf_btn.setToolTip(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Informations complémentaires</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">(activité, invalidité, garde alternée)</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.inf_btn.setText(_fromUtf8(""))
        icon5 = QtGui.QIcon()
        icon5.addPixmap(QtGui.QPixmap(_fromUtf8(":/images/people.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.inf_btn.setIcon(icon5)
        self.inf_btn.setIconSize(QtCore.QSize(22, 22))
        self.inf_btn.setObjectName(_fromUtf8("inf_btn"))
        self.horizontalLayout.addWidget(self.inf_btn)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.line = QtGui.QFrame(self.dockWidgetContents)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout.addWidget(self.line)
        self.scrollArea = QtGui.QScrollArea(self.dockWidgetContents)
        self.scrollArea.setMinimumSize(QtCore.QSize(375, 100))
        self.scrollArea.setFrameShape(QtGui.QFrame.StyledPanel)
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        self.scrollArea.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 356, 116))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setSpacing(0)
        self.verticalLayout_2.setMargin(0)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label_8 = QtGui.QLabel(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_8.sizePolicy().hasHeightForWidth())
        self.label_8.setSizePolicy(sizePolicy)
        self.label_8.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">n°</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 0, 0, 2, 1)
        self.label_4 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_4.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Date de </span></p>\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">naissance</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 0, 1, 2, 1)
        self.label_11 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_11.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Déclaration d\'impôts</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_11.setObjectName(_fromUtf8("label_11"))
        self.gridLayout.addWidget(self.label_11, 0, 2, 1, 3)
        self.label_12 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_12.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt; font-weight:600;\">Famille</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.gridLayout.addWidget(self.label_12, 0, 5, 1, 2)
        self.label_6 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_6.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Numéro</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 1, 2, 1, 1)
        self.label_7 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_7.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Position</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 1, 3, 1, 1)
        self.label_10 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_10.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Remplir</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_10.setObjectName(_fromUtf8("label_10"))
        self.gridLayout.addWidget(self.label_10, 1, 4, 1, 1)
        self.label_5 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_5.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Numéro</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 1, 5, 1, 1)
        self.label_9 = QtGui.QLabel(self.scrollAreaWidgetContents)
        self.label_9.setText(QtGui.QApplication.translate("Menage", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'MS Shell Dlg 2\'; font-size:8.25pt; font-weight:400; font-style:normal;\">\n"
"<p align=\"center\" style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-size:8pt;\">Position</span></p></body></html>", None, QtGui.QApplication.UnicodeUTF8))
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 6, 1, 1)
        self.verticalLayout_2.addLayout(self.gridLayout)
        spacerItem1 = QtGui.QSpacerItem(20, 297, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem1)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        Menage.setWidget(self.dockWidgetContents)

        self.retranslateUi(Menage)
        QtCore.QMetaObject.connectSlotsByName(Menage)

    def retranslateUi(self, Menage):
        pass

import resources_rc

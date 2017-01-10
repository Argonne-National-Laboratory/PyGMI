# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyGMI_files\Config_menu.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Config_menu(object):
    def setupUi(self, Config_menu):
        Config_menu.setObjectName(_fromUtf8("Config_menu"))
        Config_menu.resize(543, 593)
        self.gridLayout = QtGui.QGridLayout(Config_menu)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Config_menu)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.macfold = QtGui.QLineEdit(Config_menu)
        self.macfold.setObjectName(_fromUtf8("macfold"))
        self.gridLayout.addWidget(self.macfold, 1, 0, 1, 6)
        self.label_2 = QtGui.QLabel(Config_menu)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 2)
        self.measfold = QtGui.QLineEdit(Config_menu)
        self.measfold.setObjectName(_fromUtf8("measfold"))
        self.gridLayout.addWidget(self.measfold, 3, 0, 1, 6)
        self.label_4 = QtGui.QLabel(Config_menu)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.gridLayout.addWidget(self.label_4, 7, 0, 1, 2)
        self.smtpadd = QtGui.QLineEdit(Config_menu)
        self.smtpadd.setObjectName(_fromUtf8("smtpadd"))
        self.gridLayout.addWidget(self.smtpadd, 8, 0, 1, 6)
        self.label_5 = QtGui.QLabel(Config_menu)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.gridLayout.addWidget(self.label_5, 9, 0, 1, 2)
        self.login = QtGui.QLineEdit(Config_menu)
        self.login.setObjectName(_fromUtf8("login"))
        self.gridLayout.addWidget(self.login, 10, 0, 1, 6)
        self.label_6 = QtGui.QLabel(Config_menu)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 11, 0, 1, 2)
        self.mdp = QtGui.QLineEdit(Config_menu)
        self.mdp.setEchoMode(QtGui.QLineEdit.Password)
        self.mdp.setObjectName(_fromUtf8("mdp"))
        self.gridLayout.addWidget(self.mdp, 12, 0, 1, 6)
        self.label_7 = QtGui.QLabel(Config_menu)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.gridLayout.addWidget(self.label_7, 13, 0, 1, 2)
        self.pushButton = QtGui.QPushButton(Config_menu)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 15, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Config_menu)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 15, 1, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Config_menu)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 17, 4, 1, 2)
        self.label_3 = QtGui.QLabel(Config_menu)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 5, 0, 1, 1)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem, 4, 0, 1, 1)
        self.pointsize = QtGui.QSpinBox(Config_menu)
        self.pointsize.setObjectName(_fromUtf8("pointsize"))
        self.gridLayout.addWidget(self.pointsize, 15, 3, 1, 1)
        self.label_8 = QtGui.QLabel(Config_menu)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.gridLayout.addWidget(self.label_8, 15, 2, 1, 1)
        self.pushButton_4 = QtGui.QPushButton(Config_menu)
        self.pushButton_4.setObjectName(_fromUtf8("pushButton_4"))
        self.gridLayout.addWidget(self.pushButton_4, 17, 0, 1, 1)
        self.pushButton_3 = QtGui.QPushButton(Config_menu)
        self.pushButton_3.setObjectName(_fromUtf8("pushButton_3"))
        self.gridLayout.addWidget(self.pushButton_3, 17, 1, 1, 1)
        spacerItem1 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        self.gridLayout.addItem(spacerItem1, 16, 0, 1, 1)
        self.label_9 = QtGui.QLabel(Config_menu)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 7, 4, 1, 1)
        self.smtpport = QtGui.QSpinBox(Config_menu)
        self.smtpport.setMaximum(100000)
        self.smtpport.setProperty("value", 465)
        self.smtpport.setObjectName(_fromUtf8("smtpport"))
        self.gridLayout.addWidget(self.smtpport, 7, 5, 1, 1)

        self.retranslateUi(Config_menu)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Config_menu.update_values)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Config_menu.reject)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Config_menu.change_line_color)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Config_menu.change_point_color)
        QtCore.QObject.connect(self.pushButton_3, QtCore.SIGNAL(_fromUtf8("clicked()")), Config_menu.loadconf)
        QtCore.QObject.connect(self.pushButton_4, QtCore.SIGNAL(_fromUtf8("clicked()")), Config_menu.saveconf)
        QtCore.QMetaObject.connectSlotsByName(Config_menu)

    def retranslateUi(self, Config_menu):
        Config_menu.setWindowTitle(_translate("Config_menu", "Dialog", None))
        self.label.setText(_translate("Config_menu", "default macro folder", None))
        self.macfold.setText(_translate("Config_menu", "macro", None))
        self.label_2.setText(_translate("Config_menu", "default data files folder", None))
        self.measfold.setText(_translate("Config_menu", "measurements data", None))
        self.label_4.setText(_translate("Config_menu", "Smtp server address", None))
        self.smtpadd.setText(_translate("Config_menu", "smtp.mail.com", None))
        self.label_5.setText(_translate("Config_menu", "Login", None))
        self.login.setText(_translate("Config_menu", "blabla@blabla.com", None))
        self.label_6.setText(_translate("Config_menu", "Password", None))
        self.mdp.setText(_translate("Config_menu", "Password", None))
        self.label_7.setText(_translate("Config_menu", "Plot default options", None))
        self.pushButton.setText(_translate("Config_menu", "Line color", None))
        self.pushButton_2.setText(_translate("Config_menu", "Point color", None))
        self.label_3.setText(_translate("Config_menu", "e-mail", None))
        self.label_8.setText(_translate("Config_menu", "Point size", None))
        self.pushButton_4.setText(_translate("Config_menu", "Save", None))
        self.pushButton_3.setText(_translate("Config_menu", "Load", None))
        self.label_9.setText(_translate("Config_menu", "Port", None))


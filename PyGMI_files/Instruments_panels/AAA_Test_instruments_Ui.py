# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Users\leroux\Github\PyGMI\PyGMI_files\Instruments_panels\AAA_Test_instruments.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Panel(object):
    def setupUi(self, Panel):
        Panel.setObjectName("Panel")
        Panel.resize(413, 183)
        self.gridLayout = QtWidgets.QGridLayout(Panel)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_7 = QtWidgets.QPushButton(Panel)
        self.pushButton_7.setDefault(False)
        self.pushButton_7.setObjectName("pushButton_7")
        self.gridLayout.addWidget(self.pushButton_7, 1, 2, 1, 1)
        self.temp_controller_setpoint = QtWidgets.QDoubleSpinBox(Panel)
        self.temp_controller_setpoint.setMinimumSize(QtCore.QSize(91, 0))
        self.temp_controller_setpoint.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_setpoint.setDecimals(3)
        self.temp_controller_setpoint.setMaximum(330.0)
        self.temp_controller_setpoint.setSingleStep(0.1)
        self.temp_controller_setpoint.setProperty("value", 2.0)
        self.temp_controller_setpoint.setObjectName("temp_controller_setpoint")
        self.gridLayout.addWidget(self.temp_controller_setpoint, 4, 2, 1, 1)
        self.label_75 = QtWidgets.QLabel(Panel)
        self.label_75.setObjectName("label_75")
        self.gridLayout.addWidget(self.label_75, 5, 1, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_72 = QtWidgets.QLabel(Panel)
        self.label_72.setObjectName("label_72")
        self.gridLayout.addWidget(self.label_72, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.pushButton_6 = QtWidgets.QPushButton(Panel)
        self.pushButton_6.setDefault(False)
        self.pushButton_6.setObjectName("pushButton_6")
        self.gridLayout.addWidget(self.pushButton_6, 4, 3, 1, 1)
        self.temp_controller_P = QtWidgets.QDoubleSpinBox(Panel)
        self.temp_controller_P.setMinimumSize(QtCore.QSize(91, 0))
        self.temp_controller_P.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_P.setSuffix("")
        self.temp_controller_P.setDecimals(3)
        self.temp_controller_P.setMaximum(9999999.0)
        self.temp_controller_P.setSingleStep(0.1)
        self.temp_controller_P.setProperty("value", 0.0)
        self.temp_controller_P.setObjectName("temp_controller_P")
        self.gridLayout.addWidget(self.temp_controller_P, 6, 0, 1, 1)
        self.temp_controller_I = QtWidgets.QDoubleSpinBox(Panel)
        self.temp_controller_I.setMinimumSize(QtCore.QSize(91, 0))
        self.temp_controller_I.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_I.setSuffix("")
        self.temp_controller_I.setDecimals(3)
        self.temp_controller_I.setMaximum(9999999.0)
        self.temp_controller_I.setSingleStep(10.0)
        self.temp_controller_I.setProperty("value", 0.0)
        self.temp_controller_I.setObjectName("temp_controller_I")
        self.gridLayout.addWidget(self.temp_controller_I, 6, 1, 1, 1)
        self.temp_controller_loop = QtWidgets.QSpinBox(Panel)
        self.temp_controller_loop.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_loop.setMinimum(1)
        self.temp_controller_loop.setObjectName("temp_controller_loop")
        self.gridLayout.addWidget(self.temp_controller_loop, 4, 1, 1, 1)
        self.temp_controller_D = QtWidgets.QDoubleSpinBox(Panel)
        self.temp_controller_D.setMinimumSize(QtCore.QSize(91, 0))
        self.temp_controller_D.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_D.setSuffix("")
        self.temp_controller_D.setDecimals(3)
        self.temp_controller_D.setMaximum(9999999.0)
        self.temp_controller_D.setSingleStep(1.0)
        self.temp_controller_D.setProperty("value", 0.0)
        self.temp_controller_D.setObjectName("temp_controller_D")
        self.gridLayout.addWidget(self.temp_controller_D, 6, 2, 1, 1)
        self.temp_controller_channel = QtWidgets.QComboBox(Panel)
        self.temp_controller_channel.setObjectName("temp_controller_channel")
        self.temp_controller_channel.addItem("")
        self.temp_controller_channel.addItem("")
        self.temp_controller_channel.addItem("")
        self.temp_controller_channel.addItem("")
        self.gridLayout.addWidget(self.temp_controller_channel, 4, 0, 1, 1)
        self.temp_controller_ramprate = QtWidgets.QDoubleSpinBox(Panel)
        self.temp_controller_ramprate.setMinimumSize(QtCore.QSize(91, 0))
        self.temp_controller_ramprate.setAlignment(QtCore.Qt.AlignCenter)
        self.temp_controller_ramprate.setDecimals(2)
        self.temp_controller_ramprate.setMaximum(200000.0)
        self.temp_controller_ramprate.setSingleStep(1.0)
        self.temp_controller_ramprate.setProperty("value", 10.0)
        self.temp_controller_ramprate.setObjectName("temp_controller_ramprate")
        self.gridLayout.addWidget(self.temp_controller_ramprate, 1, 0, 1, 1)
        self.label_45 = QtWidgets.QLabel(Panel)
        self.label_45.setObjectName("label_45")
        self.gridLayout.addWidget(self.label_45, 0, 0, 1, 1)
        self.pushButton_5 = QtWidgets.QPushButton(Panel)
        self.pushButton_5.setDefault(False)
        self.pushButton_5.setObjectName("pushButton_5")
        self.gridLayout.addWidget(self.pushButton_5, 1, 1, 1, 1)
        self.label_76 = QtWidgets.QLabel(Panel)
        self.label_76.setObjectName("label_76")
        self.gridLayout.addWidget(self.label_76, 5, 2, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_46 = QtWidgets.QLabel(Panel)
        self.label_46.setObjectName("label_46")
        self.gridLayout.addWidget(self.label_46, 3, 1, 1, 1)
        self.label_24 = QtWidgets.QLabel(Panel)
        self.label_24.setObjectName("label_24")
        self.gridLayout.addWidget(self.label_24, 3, 0, 1, 1)
        self.label_44 = QtWidgets.QLabel(Panel)
        self.label_44.setObjectName("label_44")
        self.gridLayout.addWidget(self.label_44, 3, 2, 1, 1)

        self.retranslateUi(Panel)
        QtCore.QMetaObject.connectSlotsByName(Panel)

    def retranslateUi(self, Panel):
        _translate = QtCore.QCoreApplication.translate
        Panel.setWindowTitle(_translate("Panel", "Lakeshore - 340"))
        self.pushButton_7.setText(_translate("Panel", "OFF"))
        self.temp_controller_setpoint.setSuffix(_translate("Panel", " K"))
        self.label_75.setText(_translate("Panel", "I"))
        self.label_72.setText(_translate("Panel", "P"))
        self.pushButton_6.setText(_translate("Panel", "Set"))
        self.temp_controller_loop.setPrefix(_translate("Panel", "loop "))
        self.temp_controller_channel.setItemText(0, _translate("Panel", "A"))
        self.temp_controller_channel.setItemText(1, _translate("Panel", "B"))
        self.temp_controller_channel.setItemText(2, _translate("Panel", "C"))
        self.temp_controller_channel.setItemText(3, _translate("Panel", "D"))
        self.temp_controller_ramprate.setSuffix(_translate("Panel", " K/min"))
        self.label_45.setText(_translate("Panel", "Ramp Rate"))
        self.pushButton_5.setText(_translate("Panel", "ON"))
        self.label_76.setText(_translate("Panel", "D"))
        self.label_46.setText(_translate("Panel", "Control loop"))
        self.label_24.setText(_translate("Panel", "Channel"))
        self.label_44.setText(_translate("Panel", "Setpoint"))


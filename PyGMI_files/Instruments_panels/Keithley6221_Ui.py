# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyGMI_files\Instruments_panels\Keithley6221.ui'
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

class Ui_Panel(object):
    def setupUi(self, Panel):
        Panel.setObjectName(_fromUtf8("Panel"))
        Panel.resize(479, 70)
        self.gridLayout = QtGui.QGridLayout(Panel)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.I_disp = QtGui.QLabel(Panel)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.I_disp.setFont(font)
        self.I_disp.setAutoFillBackground(False)
        self.I_disp.setStyleSheet(_fromUtf8("background-color: rgb(0, 1, 0);\n"
"color: rgb(250, 28, 51);"))
        self.I_disp.setFrameShape(QtGui.QFrame.WinPanel)
        self.I_disp.setFrameShadow(QtGui.QFrame.Sunken)
        self.I_disp.setScaledContents(False)
        self.I_disp.setAlignment(QtCore.Qt.AlignCenter)
        self.I_disp.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.I_disp.setObjectName(_fromUtf8("I_disp"))
        self.gridLayout.addWidget(self.I_disp, 0, 0, 1, 1)
        self.doubleSpinBox = QtGui.QDoubleSpinBox(Panel)
        self.doubleSpinBox.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox.setDecimals(1)
        self.doubleSpinBox.setMinimum(-1000000.0)
        self.doubleSpinBox.setMaximum(1000000.0)
        self.doubleSpinBox.setSingleStep(50.0)
        self.doubleSpinBox.setObjectName(_fromUtf8("doubleSpinBox"))
        self.gridLayout.addWidget(self.doubleSpinBox, 0, 1, 1, 1)
        self.outputON = QtGui.QRadioButton(Panel)
        self.outputON.setObjectName(_fromUtf8("outputON"))
        self.gridLayout.addWidget(self.outputON, 0, 2, 1, 1)
        self.label_47 = QtGui.QLabel(Panel)
        self.label_47.setAlignment(QtCore.Qt.AlignCenter)
        self.label_47.setObjectName(_fromUtf8("label_47"))
        self.gridLayout.addWidget(self.label_47, 0, 3, 1, 1)
        self.monitor = QtGui.QCheckBox(Panel)
        self.monitor.setChecked(False)
        self.monitor.setObjectName(_fromUtf8("monitor"))
        self.gridLayout.addWidget(self.monitor, 0, 4, 1, 1)
        self.V_disp = QtGui.QLabel(Panel)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Courier"))
        font.setBold(True)
        font.setWeight(75)
        font.setKerning(True)
        self.V_disp.setFont(font)
        self.V_disp.setAutoFillBackground(False)
        self.V_disp.setStyleSheet(_fromUtf8("background-color: rgb(0, 1, 0);\n"
"color: rgb(250, 28, 51);"))
        self.V_disp.setFrameShape(QtGui.QFrame.WinPanel)
        self.V_disp.setFrameShadow(QtGui.QFrame.Sunken)
        self.V_disp.setScaledContents(False)
        self.V_disp.setAlignment(QtCore.Qt.AlignCenter)
        self.V_disp.setTextInteractionFlags(QtCore.Qt.TextSelectableByMouse)
        self.V_disp.setObjectName(_fromUtf8("V_disp"))
        self.gridLayout.addWidget(self.V_disp, 1, 0, 1, 1)
        self.doubleSpinBox_2 = QtGui.QDoubleSpinBox(Panel)
        self.doubleSpinBox_2.setAlignment(QtCore.Qt.AlignCenter)
        self.doubleSpinBox_2.setDecimals(3)
        self.doubleSpinBox_2.setMinimum(-50.0)
        self.doubleSpinBox_2.setMaximum(50.0)
        self.doubleSpinBox_2.setSingleStep(1.0)
        self.doubleSpinBox_2.setProperty("value", 10.0)
        self.doubleSpinBox_2.setObjectName(_fromUtf8("doubleSpinBox_2"))
        self.gridLayout.addWidget(self.doubleSpinBox_2, 1, 1, 1, 1)
        self.resetbutton = QtGui.QPushButton(Panel)
        self.resetbutton.setObjectName(_fromUtf8("resetbutton"))
        self.gridLayout.addWidget(self.resetbutton, 1, 2, 1, 1)
        self.refresh_rate = QtGui.QDoubleSpinBox(Panel)
        self.refresh_rate.setMinimumSize(QtCore.QSize(91, 0))
        self.refresh_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.refresh_rate.setDecimals(1)
        self.refresh_rate.setMaximum(9999999.0)
        self.refresh_rate.setSingleStep(0.5)
        self.refresh_rate.setProperty("value", 2.0)
        self.refresh_rate.setObjectName(_fromUtf8("refresh_rate"))
        self.gridLayout.addWidget(self.refresh_rate, 1, 3, 1, 2)

        self.retranslateUi(Panel)
        QtCore.QObject.connect(self.monitor, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Panel.monitor)
        QtCore.QObject.connect(self.refresh_rate, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Panel.update_timer_timeout)
        QtCore.QObject.connect(self.doubleSpinBox, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Panel.change_I)
        QtCore.QObject.connect(self.doubleSpinBox_2, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Panel.change_V_comp)
        QtCore.QObject.connect(self.outputON, QtCore.SIGNAL(_fromUtf8("clicked(bool)")), Panel.switch_output)
        QtCore.QObject.connect(self.resetbutton, QtCore.SIGNAL(_fromUtf8("clicked()")), Panel.reset_inst)
        QtCore.QMetaObject.connectSlotsByName(Panel)

    def retranslateUi(self, Panel):
        Panel.setWindowTitle(_translate("Panel", "Keithley 6221", None))
        self.I_disp.setText(_translate("Panel", "--- μA", None))
        self.doubleSpinBox.setSuffix(_translate("Panel", " μA", None))
        self.outputON.setText(_translate("Panel", "Output ON", None))
        self.label_47.setText(_translate("Panel", "Refresh rate", None))
        self.monitor.setText(_translate("Panel", "Monitor", None))
        self.V_disp.setText(_translate("Panel", "--- V", None))
        self.doubleSpinBox_2.setSuffix(_translate("Panel", " V", None))
        self.resetbutton.setText(_translate("Panel", "Reset", None))
        self.refresh_rate.setSuffix(_translate("Panel", " secs", None))


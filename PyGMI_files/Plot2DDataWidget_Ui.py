# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyGMI_files\Plot2DDataWidget.ui'
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

class Ui_Plot2DData(object):
    def setupUi(self, Plot2DData):
        Plot2DData.setObjectName(_fromUtf8("Plot2DData"))
        Plot2DData.resize(707, 753)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Plot2DData.sizePolicy().hasHeightForWidth())
        Plot2DData.setSizePolicy(sizePolicy)
        self.gridLayout = QtGui.QGridLayout(Plot2DData)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.plot_area = PlotWidget(Plot2DData)
        self.plot_area.setObjectName(_fromUtf8("plot_area"))
        self.gridLayout.addWidget(self.plot_area, 0, 0, 1, 4)
        self.label_3 = QtGui.QLabel(Plot2DData)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_3.setFont(font)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 1, 0, 1, 1)
        self.y_axis_box = QtGui.QComboBox(Plot2DData)
        self.y_axis_box.setObjectName(_fromUtf8("y_axis_box"))
        self.gridLayout.addWidget(self.y_axis_box, 1, 1, 1, 1)
        self.label_9 = QtGui.QLabel(Plot2DData)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(12)
        self.label_9.setFont(font)
        self.label_9.setAlignment(QtCore.Qt.AlignCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.gridLayout.addWidget(self.label_9, 1, 2, 1, 1)
        self.x_axis_box = QtGui.QComboBox(Plot2DData)
        self.x_axis_box.setObjectName(_fromUtf8("x_axis_box"))
        self.gridLayout.addWidget(self.x_axis_box, 1, 3, 1, 1)
        self.pushButton = QtGui.QPushButton(Plot2DData)
        self.pushButton.setObjectName(_fromUtf8("pushButton"))
        self.gridLayout.addWidget(self.pushButton, 2, 0, 1, 1)
        self.pushButton_2 = QtGui.QPushButton(Plot2DData)
        self.pushButton_2.setObjectName(_fromUtf8("pushButton_2"))
        self.gridLayout.addWidget(self.pushButton_2, 2, 1, 1, 1)
        self.label_6 = QtGui.QLabel(Plot2DData)
        self.label_6.setAlignment(QtCore.Qt.AlignCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.gridLayout.addWidget(self.label_6, 2, 2, 1, 1)
        self.refresh_rate = QtGui.QDoubleSpinBox(Plot2DData)
        self.refresh_rate.setMinimumSize(QtCore.QSize(91, 0))
        self.refresh_rate.setAlignment(QtCore.Qt.AlignCenter)
        self.refresh_rate.setPrefix(_fromUtf8(""))
        self.refresh_rate.setDecimals(1)
        self.refresh_rate.setMinimum(0.1)
        self.refresh_rate.setMaximum(200000.0)
        self.refresh_rate.setSingleStep(0.5)
        self.refresh_rate.setProperty("value", 0.5)
        self.refresh_rate.setObjectName(_fromUtf8("refresh_rate"))
        self.gridLayout.addWidget(self.refresh_rate, 2, 3, 1, 1)
        self.label = QtGui.QLabel(Plot2DData)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 3, 0, 1, 1)
        self.Symbol_size = QtGui.QSpinBox(Plot2DData)
        self.Symbol_size.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.Symbol_size.setSuffix(_fromUtf8(""))
        self.Symbol_size.setPrefix(_fromUtf8(""))
        self.Symbol_size.setProperty("value", 0)
        self.Symbol_size.setObjectName(_fromUtf8("Symbol_size"))
        self.gridLayout.addWidget(self.Symbol_size, 3, 1, 1, 1)
        self.auto_upd = QtGui.QCheckBox(Plot2DData)
        self.auto_upd.setChecked(True)
        self.auto_upd.setObjectName(_fromUtf8("auto_upd"))
        self.gridLayout.addWidget(self.auto_upd, 3, 3, 1, 1)
        self.autoconnect = QtGui.QCheckBox(Plot2DData)
        self.autoconnect.setChecked(True)
        self.autoconnect.setObjectName(_fromUtf8("autoconnect"))
        self.gridLayout.addWidget(self.autoconnect, 3, 2, 1, 1)

        self.retranslateUi(Plot2DData)
        QtCore.QObject.connect(self.y_axis_box, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), Plot2DData.updateY)
        QtCore.QObject.connect(self.x_axis_box, QtCore.SIGNAL(_fromUtf8("currentIndexChanged(int)")), Plot2DData.updateX)
        QtCore.QObject.connect(self.refresh_rate, QtCore.SIGNAL(_fromUtf8("valueChanged(double)")), Plot2DData.update_timer_timeout)
        QtCore.QObject.connect(self.Symbol_size, QtCore.SIGNAL(_fromUtf8("valueChanged(int)")), Plot2DData.change_symbol_size)
        QtCore.QObject.connect(self.pushButton_2, QtCore.SIGNAL(_fromUtf8("clicked()")), Plot2DData.change_point_color)
        QtCore.QObject.connect(self.pushButton, QtCore.SIGNAL(_fromUtf8("clicked()")), Plot2DData.change_line_color)
        QtCore.QObject.connect(self.auto_upd, QtCore.SIGNAL(_fromUtf8("stateChanged(int)")), Plot2DData.autoupdate)
        QtCore.QMetaObject.connectSlotsByName(Plot2DData)

    def retranslateUi(self, Plot2DData):
        Plot2DData.setWindowTitle(_translate("Plot2DData", "Form", None))
        self.label_3.setText(_translate("Plot2DData", "Y-axis", None))
        self.label_9.setText(_translate("Plot2DData", "X-axis", None))
        self.pushButton.setText(_translate("Plot2DData", "Line Color", None))
        self.pushButton_2.setText(_translate("Plot2DData", "Point Color", None))
        self.label_6.setText(_translate("Plot2DData", "Refresh rate", None))
        self.refresh_rate.setSuffix(_translate("Plot2DData", " s", None))
        self.label.setText(_translate("Plot2DData", "Point Size    ", None))
        self.auto_upd.setText(_translate("Plot2DData", "Auto-update", None))
        self.autoconnect.setText(_translate("Plot2DData", "Auto-connect", None))

from pyqtgraph import PlotWidget

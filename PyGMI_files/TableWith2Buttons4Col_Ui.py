# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyGMI_files\TableWith2Buttons4Col.ui'
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

class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName(_fromUtf8("Table"))
        Table.resize(427, 476)
        self.gridLayout = QtGui.QGridLayout(Table)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pushButton_18 = QtGui.QPushButton(Table)
        self.pushButton_18.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy)
        self.pushButton_18.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_18.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_18.setStyleSheet(_fromUtf8("color: rgb(0, 170, 127);\n"
"font: 26pt \"Arial\";"))
        self.pushButton_18.setDefault(False)
        self.pushButton_18.setObjectName(_fromUtf8("pushButton_18"))
        self.gridLayout.addWidget(self.pushButton_18, 0, 0, 1, 1)
        self.pushButton_17 = QtGui.QPushButton(Table)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_17.setStyleSheet(_fromUtf8("color: rgb(255, 0, 0);\n"
"font: 26pt \"Arial\";"))
        self.pushButton_17.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_17.setDefault(False)
        self.pushButton_17.setObjectName(_fromUtf8("pushButton_17"))
        self.gridLayout.addWidget(self.pushButton_17, 0, 1, 1, 1)
        self.table = QtGui.QTableWidget(Table)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.table.sizePolicy().hasHeightForWidth())
        self.table.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.table.setFont(font)
        self.table.viewport().setProperty("cursor", QtGui.QCursor(QtCore.Qt.IBeamCursor))
        self.table.setLineWidth(1)
        self.table.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.table.setAlternatingRowColors(True)
        self.table.setGridStyle(QtCore.Qt.SolidLine)
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setObjectName(_fromUtf8("table"))
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("MS Shell Dlg 2"))
        font.setPointSize(9)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        font = QtGui.QFont()
        font.setPointSize(9)
        item.setFont(font)
        self.table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignHCenter|QtCore.Qt.AlignVCenter|QtCore.Qt.AlignCenter)
        self.table.setHorizontalHeaderItem(3, item)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 3)

        self.retranslateUi(Table)
        QtCore.QObject.connect(self.pushButton_18, QtCore.SIGNAL(_fromUtf8("clicked()")), Table.insert_row)
        QtCore.QObject.connect(self.pushButton_17, QtCore.SIGNAL(_fromUtf8("clicked()")), Table.delete_row)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        Table.setWindowTitle(_translate("Table", "Form", None))
        self.pushButton_18.setText(_translate("Table", "+", None))
        self.pushButton_17.setText(_translate("Table", "-", None))
        item = self.table.horizontalHeaderItem(0)
        item.setText(_translate("Table", "From", None))
        item = self.table.horizontalHeaderItem(1)
        item.setText(_translate("Table", "To", None))
        item = self.table.horizontalHeaderItem(2)
        item.setText(_translate("Table", "step", None))
        item = self.table.horizontalHeaderItem(3)
        item.setText(_translate("Table", "rate", None))


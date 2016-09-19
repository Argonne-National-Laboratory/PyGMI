# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'TableWith2Buttons4Col.ui'
#
# Created: Mon Oct 20 23:34:23 2014
#      by: pyside-uic 0.2.15 running on PySide 1.2.2
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Table(object):
    def setupUi(self, Table):
        Table.setObjectName("Table")
        Table.resize(427, 476)
        self.gridLayout = QtGui.QGridLayout(Table)
        self.gridLayout.setObjectName("gridLayout")
        self.pushButton_18 = QtGui.QPushButton(Table)
        self.pushButton_18.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_18.sizePolicy().hasHeightForWidth())
        self.pushButton_18.setSizePolicy(sizePolicy)
        self.pushButton_18.setMinimumSize(QtCore.QSize(30, 30))
        self.pushButton_18.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_18.setStyleSheet("color: rgb(0, 170, 127);\n"
"font: 26pt \"Arial\";")
        self.pushButton_18.setDefault(False)
        self.pushButton_18.setObjectName("pushButton_18")
        self.gridLayout.addWidget(self.pushButton_18, 0, 0, 1, 1)
        self.pushButton_17 = QtGui.QPushButton(Table)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_17.sizePolicy().hasHeightForWidth())
        self.pushButton_17.setSizePolicy(sizePolicy)
        self.pushButton_17.setMaximumSize(QtCore.QSize(30, 30))
        self.pushButton_17.setStyleSheet("color: rgb(255, 0, 0);\n"
"font: 26pt \"Arial\";")
        self.pushButton_17.setIconSize(QtCore.QSize(20, 20))
        self.pushButton_17.setDefault(False)
        self.pushButton_17.setObjectName("pushButton_17")
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
        self.table.setProperty("cursor", QtCore.Qt.IBeamCursor)
        self.table.setLineWidth(1)
        self.table.setDragDropMode(QtGui.QAbstractItemView.DragDrop)
        self.table.setAlternatingRowColors(True)
        self.table.setGridStyle(QtCore.Qt.SolidLine)
        self.table.setRowCount(1)
        self.table.setColumnCount(4)
        self.table.setObjectName("table")
        self.table.setColumnCount(4)
        self.table.setRowCount(1)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.table.setHorizontalHeaderItem(3, item)
        self.table.horizontalHeader().setCascadingSectionResizes(True)
        self.table.horizontalHeader().setDefaultSectionSize(100)
        self.table.horizontalHeader().setStretchLastSection(False)
        self.table.verticalHeader().setVisible(False)
        self.table.verticalHeader().setStretchLastSection(False)
        self.gridLayout.addWidget(self.table, 1, 0, 1, 3)

        self.retranslateUi(Table)
        QtCore.QObject.connect(self.pushButton_18, QtCore.SIGNAL("clicked()"), Table.insert_row)
        QtCore.QObject.connect(self.pushButton_17, QtCore.SIGNAL("clicked()"), Table.delete_row)
        QtCore.QMetaObject.connectSlotsByName(Table)

    def retranslateUi(self, Table):
        Table.setWindowTitle(QtGui.QApplication.translate("Table", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_18.setText(QtGui.QApplication.translate("Table", "+", None, QtGui.QApplication.UnicodeUTF8))
        self.pushButton_17.setText(QtGui.QApplication.translate("Table", "-", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(0).setText(QtGui.QApplication.translate("Table", "From", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(1).setText(QtGui.QApplication.translate("Table", "To", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(2).setText(QtGui.QApplication.translate("Table", "step", None, QtGui.QApplication.UnicodeUTF8))
        self.table.horizontalHeaderItem(3).setText(QtGui.QApplication.translate("Table", "rate", None, QtGui.QApplication.UnicodeUTF8))


# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'PyGMI_files\Macro_editor.ui'
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

class Ui_Macro_editor(object):
    def setupUi(self, Macro_editor):
        Macro_editor.setObjectName(_fromUtf8("Macro_editor"))
        Macro_editor.resize(1044, 806)
        self.gridLayout = QtGui.QGridLayout(Macro_editor)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.macro_textbox = MyMacroEdit(Macro_editor)
        self.macro_textbox.setLineWrapMode(QtGui.QPlainTextEdit.WidgetWidth)
        self.macro_textbox.setBackgroundVisible(False)
        self.macro_textbox.setObjectName(_fromUtf8("macro_textbox"))
        self.gridLayout.addWidget(self.macro_textbox, 0, 0, 1, 3)
        self.macrocommandtree = QtGui.QTreeView(Macro_editor)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.macrocommandtree.sizePolicy().hasHeightForWidth())
        self.macrocommandtree.setSizePolicy(sizePolicy)
        self.macrocommandtree.setProperty("showDropIndicator", False)
        self.macrocommandtree.setAlternatingRowColors(True)
        self.macrocommandtree.setTextElideMode(QtCore.Qt.ElideRight)
        self.macrocommandtree.setRootIsDecorated(True)
        self.macrocommandtree.setUniformRowHeights(False)
        self.macrocommandtree.setItemsExpandable(True)
        self.macrocommandtree.setAnimated(False)
        self.macrocommandtree.setWordWrap(True)
        self.macrocommandtree.setExpandsOnDoubleClick(True)
        self.macrocommandtree.setObjectName(_fromUtf8("macrocommandtree"))
        self.macrocommandtree.header().setHighlightSections(True)
        self.gridLayout.addWidget(self.macrocommandtree, 0, 3, 1, 1)
        self.label_2 = QtGui.QLabel(Macro_editor)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.mac_curr_line = QtGui.QLineEdit(Macro_editor)
        self.mac_curr_line.setEnabled(False)
        self.mac_curr_line.setObjectName(_fromUtf8("mac_curr_line"))
        self.gridLayout.addWidget(self.mac_curr_line, 2, 0, 1, 3)
        self.pushButton_8 = QtGui.QPushButton(Macro_editor)
        self.pushButton_8.setDefault(False)
        self.pushButton_8.setObjectName(_fromUtf8("pushButton_8"))
        self.gridLayout.addWidget(self.pushButton_8, 3, 0, 1, 1)
        self.pushButton_9 = QtGui.QPushButton(Macro_editor)
        self.pushButton_9.setDefault(False)
        self.pushButton_9.setObjectName(_fromUtf8("pushButton_9"))
        self.gridLayout.addWidget(self.pushButton_9, 3, 1, 1, 1)
        self.pushButton_10 = QtGui.QPushButton(Macro_editor)
        self.pushButton_10.setDefault(False)
        self.pushButton_10.setObjectName(_fromUtf8("pushButton_10"))
        self.gridLayout.addWidget(self.pushButton_10, 3, 2, 1, 1)
        self.pushButton_11 = QtGui.QPushButton(Macro_editor)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.pushButton_11.setFont(font)
        self.pushButton_11.setDefault(False)
        self.pushButton_11.setObjectName(_fromUtf8("pushButton_11"))
        self.gridLayout.addWidget(self.pushButton_11, 4, 0, 1, 2)
        self.pushButton_12 = QtGui.QPushButton(Macro_editor)
        self.pushButton_12.setEnabled(True)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton_12.sizePolicy().hasHeightForWidth())
        self.pushButton_12.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Arial"))
        font.setPointSize(26)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(9)
        self.pushButton_12.setFont(font)
        self.pushButton_12.setStyleSheet(_fromUtf8("background-color: rgb(255, 0, 0);\n"
"color: rgb(255, 255, 255);\n"
"font: 75 26pt \"Arial\";"))
        self.pushButton_12.setDefault(False)
        self.pushButton_12.setObjectName(_fromUtf8("pushButton_12"))
        self.gridLayout.addWidget(self.pushButton_12, 2, 3, 3, 1)

        self.retranslateUi(Macro_editor)
        QtCore.QObject.connect(self.pushButton_9, QtCore.SIGNAL(_fromUtf8("clicked()")), Macro_editor.save_macro)
        QtCore.QObject.connect(self.pushButton_8, QtCore.SIGNAL(_fromUtf8("clicked()")), Macro_editor.open_macro)
        QtCore.QObject.connect(self.pushButton_11, QtCore.SIGNAL(_fromUtf8("clicked()")), Macro_editor.run_macro)
        QtCore.QObject.connect(self.pushButton_10, QtCore.SIGNAL(_fromUtf8("clicked()")), self.macro_textbox.clear)
        QtCore.QObject.connect(self.pushButton_12, QtCore.SIGNAL(_fromUtf8("clicked()")), Macro_editor.stop_macro)
        QtCore.QMetaObject.connectSlotsByName(Macro_editor)

    def retranslateUi(self, Macro_editor):
        Macro_editor.setWindowTitle(_translate("Macro_editor", "Form", None))
        self.label_2.setText(_translate("Macro_editor", "Current line in the macro", None))
        self.pushButton_8.setText(_translate("Macro_editor", "Open Macro", None))
        self.pushButton_9.setText(_translate("Macro_editor", "Save Macro", None))
        self.pushButton_10.setText(_translate("Macro_editor", "Clear Macro", None))
        self.pushButton_11.setText(_translate("Macro_editor", "Run Macro", None))
        self.pushButton_12.setText(_translate("Macro_editor", "Stop Macro", None))

from Macro_editor_textbox import MyMacroEdit

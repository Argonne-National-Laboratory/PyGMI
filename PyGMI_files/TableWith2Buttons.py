from PyQt5.QtWidgets import QWidget,QApplication
from . import TableWith2Buttons_Ui


class TableWith2Buttons(QWidget):
    def __init__(self,parent=None,title='TableWith2Buttons'):
        # This class derivates from a Qt MainWindow so we have to call
        # the class builder ".__init__()"
        #QMainWindow.__init__(self)
        QWidget.__init__(self)
        # "self" is now a Qt Mainwindow, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = TableWith2Buttons_Ui.Ui_Table()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a Qt Mainwindow, but the widgets will actually be built as children
        # of this object (self.ui)
        self.ui.setupUi(self)
        self.setWindowTitle(title)

    def insert_row(self):
        l=self.ui.table.rowCount()
        self.ui.table.insertRow(l)
    
    def delete_row(self):
        l=self.ui.table.rowCount()
        self.ui.table.removeRow(l-1)


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = TableWith2Buttons(app)
    window.show()
    sys.exit(app.exec_())

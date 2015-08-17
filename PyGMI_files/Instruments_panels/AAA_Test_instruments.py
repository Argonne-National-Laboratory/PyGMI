# -*- coding: utf-8 -*-
from PySide.QtGui import QWidget
import AAA_Test_instruments_Ui

class Panel(QWidget):
    def __init__(self,parent=None,instr=None,lock=None,title='Instrument Panel'):
        # This class derivates from a Qt Widget so we have to call
        # the class builder ".__init__()"
        QWidget.__init__(self)
        # "self" is now a Qt Widget, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = AAA_Test_instruments_Ui.Ui_Panel()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with the current Qt Widget 'self', but the widgets from the design will actually be built as children
        # of the object self.ui
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.reserved_access_to_instr=lock
        self.temp_controller=instr
    
    

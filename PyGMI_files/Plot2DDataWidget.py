from PySide.QtGui import QWidget,QMainWindow,QApplication,QColorDialog
from PySide.QtCore import QTimer
import Plot2DDataWidget_Ui


class Plot2DDataWidget(QWidget):
    def __init__(self,parent=None,measdata=[[1,3,2],[3,5,7]],header=["index","prime numbers"],SymbolSize=10,linecolor='y',pointcolor='b',title='Plot Window'):
        # This class derivates from a Qt MainWindow so we have to call
        # the class builder ".__init__()"
        #QMainWindow.__init__(self)
        QWidget.__init__(self)
        # "self" is now a Qt Mainwindow, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = Plot2DDataWidget_Ui.Ui_Plot2DData()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a Qt Mainwindow, but the widgets will actually be built as children
        # of this object (self.ui)
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.x_index=0
        self.y_index=0
        self.curve=self.ui.plot_area.plot(pen=linecolor)
        self.curve.setSymbolBrush(pointcolor)
        self.curve.setSymbol('o')
        self.curve.setSymbolSize(SymbolSize)
        
        self.parent=parent
        self.measdata=measdata
        self.header=header
        self.update_dropdown_boxes(header)
        
        self.update_plot_timer = QTimer()
        self.update_plot_timer.setSingleShot(True) #The timer would not wait for the completion of the task otherwise
        self.update_plot_timer.timeout.connect(self.autoupdate)

        if self.ui.auto_upd.isChecked():self.autoupdate()
            
    def update_timer_timeout(self,msec):
        self.update_plot_timer.setInterval(msec)
        
    def updateX(self,value):
        self.x_index=value
        #self.update_plot() #that was the bug
        #This created a loop because update_plot called check_connection
        #which called update_dropdown_boxes, which cleared the x_axis_box
        #which triggered a call to updateX
        
    def updateY(self,value):
        self.y_index=value
        #self.update_plot()
        
    def change_line_color(self,color=None):
        if color==None:color=QColorDialog.getColor()
        if color.isValid():
            self.curve.setPen(color)
            
    def change_point_color(self,color=None):
        if color==None:color=QColorDialog.getColor()
        if color.isValid():
            self.curve.setSymbolBrush(color)
            
    def change_symbol_size(self,value):
        self.curve.setSymbolSize(value)

    def check_connection(self,state=1):
        """check if the pointer to the Master dataset to display (self.measdata in Main.py) has changed"""
        if state and hasattr(self.parent,"measdata"):
            if self.parent.measdata!=self.measdata:self.measdata=self.parent.measdata
            if self.parent.current_header!=self.header:self.update_dropdown_boxes(self.parent.current_header)
            #print "Reestablishing connection"
    
    def autoupdate(self,state=1):
        if state:
            self.update_plot()
            self.update_plot_timer.start(self.ui.refresh_rate.value()*1000)#The value must be converted to milliseconds
        else:
            self.update_plot_timer.stop()
            
    def update_plot(self):
        """plot the data columns selected in the drop-down menu boxes"""
        if self.ui.autoconnect.isChecked():self.check_connection()
        if self.x_index!=-1 and self.y_index!=-1 and self.measdata[self.x_index]!=[] and self.measdata[self.y_index]!=[]:            
            self.curve.setData(self.measdata[self.x_index],self.measdata[self.y_index])
    
    def update_dropdown_boxes(self,header):
        """Update the drop-down boxes that select the content of the plot"""
        self.ui.x_axis_box.clear()
        self.ui.x_axis_box.addItems(header) 
        self.ui.y_axis_box.clear()
        self.ui.y_axis_box.addItems(header)
        self.header=header
        
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Plot2DDataWidget(app,[[1,3,2],[3,5,7]],["index","prime numbers"])
    window.show()
    window2 = Plot2DDataWidget(app,[[1,3,2],[3,5,7]],["index","prime numbers"])
    window2.show()
    sys.exit(app.exec_())

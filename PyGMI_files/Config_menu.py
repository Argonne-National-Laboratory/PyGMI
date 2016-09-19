from PySide.QtGui import QDialog,QMainWindow,QApplication,QColorDialog,QFileDialog,QColor
from PySide.QtCore import QTimer
import Config_menu_Ui

class Config_menu(QDialog):
    def __init__(self,parent=None,title='Configuration menu',config_dict={},debug=False):
        # This class derivates from a Qt MainWindow so we have to call
        # the class builder ".__init__()"
        #QMainWindow.__init__(self)
        QDialog.__init__(self)
        # "self" is now a Qt Mainwindow, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = Config_menu_Ui.Ui_Config_menu()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a Qt Mainwindow, but the widgets will actually be built as children
        # of this object (self.ui)
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.parent=parent
        self.config_dict=config_dict
        if not(debug):self.loadconf("./Configuration/Parameters/CurrentParameters.cfg")

    def update_values(self):
        self.config_dict['macfold']=self.ui.macfold.text().encode('utf8')
        self.config_dict['measfold']=self.ui.measfold.text().encode('utf8')
        self.config_dict['smtpadd']=self.ui.smtpadd.text().encode('utf8')
        self.config_dict['login']=self.ui.login.text().encode('utf8')
        self.config_dict['mdp']=self.ui.mdp.text().encode('utf8')
        self.config_dict['linecolor']=self.linecolor
        self.config_dict['pointcolor']=self.pointcolor
        self.config_dict['pointsize']=self.ui.pointsize.value()
        self.config_dict['smtpport']=self.ui.smtpport.value()
        self.saveconf("./Configuration/Parameters/CurrentParameters.cfg")
        self.parent.fixed_plot_conf()
        self.accept()
        
    
    def change_line_color(self):
        color=QColorDialog.getColor()
        if color.isValid():
            self.linecolor=color
            
    def change_point_color(self):
        color=QColorDialog.getColor()
        if color.isValid():
            self.pointcolor=color

    def saveconf(self,fileName=None):
        if fileName==None:
            #the static method calls the native file system
            fileName = QFileDialog.getSaveFileName(self,"Save Configuration",dir= "./Configuration/Parameters",filter="Config file (*.cfg)")
            #WARNING: write() and open() do not work with 'unicode' type object
            #they have to be converted to a string first (that is a list of bytes)
            fileName=fileName[0].encode('utf8')
        if fileName!="":
            savefile=open(fileName,'w')
            savefile.write(self.ui.macfold.text().encode('utf8')+"\n")
            savefile.write(self.ui.measfold.text().encode('utf8')+"\n")
            savefile.write(self.ui.smtpadd.text().encode('utf8')+"\n")
            savefile.write(self.ui.login.text().encode('utf8')+"\n")
            savefile.write(self.ui.mdp.text().encode('utf8')+"\n")
            savefile.write(str(self.linecolor.toTuple())+"\n")
            savefile.write(str(self.pointcolor.toTuple())+"\n")
            savefile.write(str(self.ui.pointsize.value())+"\n")
            savefile.write(str(self.ui.smtpport.value())+"\n")
            savefile.close()
        
    def loadconf(self,fileName=None):
        if fileName==None:
            fileName = QFileDialog.getOpenFileName(self,"Load Configuration",dir= "./Configuration/Parameters",filter="Config file (*.cfg)")
            #open() does not work with 'unicode' type object, conversion is needed
            fileName=fileName[0].encode('utf8')
        if fileName!="":
            file_opened=open(fileName,'r')
            self.ui.macfold.setText(file_opened.readline()[:-1])
            self.ui.measfold.setText(file_opened.readline()[:-1])
            self.ui.smtpadd.setText(file_opened.readline()[:-1])
            self.ui.login.setText(file_opened.readline()[:-1])
            self.ui.mdp.setText(file_opened.readline()[:-1])
            a=map(int,file_opened.readline()[1:-2].split(","))
            self.linecolor=QColor(a[0],a[1],a[2],a[3])
            a=map(int,file_opened.readline()[1:-2].split(","))
            self.pointcolor=QColor(a[0],a[1],a[2],a[3])
            self.ui.pointsize.setValue(int(file_opened.readline()))
            self.ui.smtpport.setValue(int(file_opened.readline()))
            file_opened.close()       


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    a={}
    window = Config_menu(app,config_dict=a,debug=True)
    window.loadconf('Parameters.cfg')
    window.show()
    #window.update_values()
    sys.exit(app.exec_())

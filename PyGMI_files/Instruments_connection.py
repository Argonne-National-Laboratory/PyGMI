from PyQt4.QtGui import QWidget,QApplication,QFileDialog,QTableWidgetItem
import Instruments_connection_Ui
import os,re,visa
import Instruments
import Instruments_panels

if __name__=='__main__':
    #The program was launched as a script,
    #so there is nothing to do, because the
    #current working directory is already set
    #to the directory of this script
    rep_module=''    
else:
    #The program was launched as a module.
    #Get the module directory name from __file__
    #which contains the absolute path of the file
    #being executed
    rep_module=os.path.dirname(__file__)+os.sep 

#find all the comboboxes of the user interface that are used to choose the instrument type.
#For that, the combobox must have a name that matches the regular expression below
#which means the combobox must be named something like : some words without space + "_instrtype_" + optionnaly some number
#e.g. "magnet_instrtype_1" or just "magnet_instrtype"
#INSTRTYPE_COMBOBOXES=re.findall(r'self\.\w+_instrtype(?:_\d+)?\.setObjectName\("(\w+_instrtype(?:_\d+)?)"\)',open(rep_module+'Instruments_connection_Ui.py').read(-1))
INSTRTYPE_COMBOBOXES=re.findall(r'self\.(\w+_instrtype(?:_\d+)?) = QtGui\.QComboBox\(Instruments_connection\)',open(rep_module+'Instruments_connection_Ui.py').read(-1))

class Instruments_connection(QWidget):
    def __init__(self,parent=None,title='Instruments Connection',debug=False):
        # This class derivates from a QWidget so we have to call
        # the class builder ".__init__()"
        QWidget.__init__(self)
        # "self" is now a QWidget, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = Instruments_connection_Ui.Ui_Instruments_connection()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a Qt Mainwindow, but the widgets will actually be built as children
        # of this object (self.ui)
        self.ui.setupUi(self)
        self.setWindowTitle(title)
        self.parent=parent
        self.connected_instr={}
        self.load_Instr_drivers_list()
        
        #if not(debug):self.loadInstrconf("./Configuration/Instruments/CurrentInstruments.cfg")

    def set_up_instr_access_lock(self,lock):
        self.reserved_access_to_instr=lock
        
    def load_Instr_drivers_list(self):
        f=self.ui
        for instr_cbb in self.list_of_all_comboboxes():
            cbb=eval("f."+instr_cbb)
            cbb.addItems(Instruments.__all__)

    def list_of_all_comboboxes(self):
        f=self.ui
#        print 'INSTRTYPE_COMBOBOXES',INSTRTYPE_COMBOBOXES
        return [eval("f."+combobox_name+".objectName()") for combobox_name in INSTRTYPE_COMBOBOXES]
        
    def list_of_all_checkboxes_pointer(self):
        f=self.ui
        return [eval("f."+instr.replace("instrtype","on")) for instr in INSTRTYPE_COMBOBOXES]

    def list_of_checked_instruments(self):
        f=self.ui
        ccbb=[]
        for combobox_name in INSTRTYPE_COMBOBOXES:
            if eval("f."+combobox_name.replace("instrtype","on")+".isChecked()"):
               ccbb.append(eval("f."+combobox_name+".objectName()"))
        return ccbb
        
    def init_instr(self):
        self.saveInstrconf("./Configuration/Instruments/CurrentInstruments.cfg")
        self.connected_instr={}
        f=self.ui
        self.shortcut_var=[]
        
        self.parent.ui.instr_mdi.closeAllSubWindows()
        with self.reserved_access_to_instr:
            for instr in self.list_of_checked_instruments():
                cbb=eval("f."+instr)#get the pointer to the combobox
                add=eval("f."+instr.replace("instrtype","visa_address")+".text()")#get the visa address
                instr_type=cbb.currentText()
                varname=instr.replace("_instrtype","")#instr_instrtype_1 -> instr_1 / magnet_Z_instrtype -> magnet_Z
                self.shortcut_var.append(varname)
                #For next upgrade : use less exec and give a dictionnary of connected instruments to be passed to the measurement programs
                #the macro mechanism will need to be updated too, as instruments won't reside in "main" anymore
                #self.connected_instr[varname]=eval("self.Instruments."+instr_type+".Connect_Instrument('"+add+"'")
                #self.connected_instr[varname].initialize()
                exec("self.parent."+varname+"=Instruments."+instr_type+".Connect_Instrument('"+add+"')")
                exec("self.parent."+varname+".initialize()")
                #if there is a panel for that type of instrument, open it in the mdi area
                if instr_type in Instruments_panels.__all__:
                    #print "creating new instrument panel"
                    sentence="newpanel=Instruments_panels."+instr_type+".Panel(self,instr=self.parent."+varname+",lock=self.reserved_access_to_instr,title='"+varname+" - "+instr_type+"')"
                    #print sentence
                    exec(sentence)
                    self.parent.ui.instr_mdi.addSubWindow(newpanel) 
                    
                                                           
    def refresh_instr_list(self):
        with self.reserved_access_to_instr:
            l=visa.ResourceManager().list_resources()
        self.ui.instr_table.setRowCount(len(l))
        for i in range(len(l)):
            if not('ASRL' in l[i] or 'COM' in l[i]):#COM ports don't respond to visa *IDN?, which raises an error, so don't ask them
                with self.reserved_access_to_instr:
                    try:
                        a=visa.ResourceManager().open_resource(l[i])
                        a.timeout=1500
                        self.ui.instr_table.setItem(i,0,QTableWidgetItem(a.query('*IDN?')))
                        a.timeout=5000
                    except:
                        self.ui.instr_table.setItem(i,0,QTableWidgetItem('Instruments did not respond to *IDN?'))
            self.ui.instr_table.setItem(i,1,QTableWidgetItem(l[i]))

    def saveInstrconf(self,fileName=None):
        if fileName==None:
            #the static method calls the native file system
            fileName = QFileDialog.getSaveFileName(self,"Save Configuration",directory = "./Configuration/Instruments",filter="Config file (*.cfg)")
            print fileName
            #PySide only
            #WARNING: write() and open() do not work with 'unicode' type object
            #they have to be converted to a string first (that is a list of bytes)
#            fileName=fileName[0].encode('utf8')
            print fileName
        if fileName!="":
            savefile=open(fileName,'w')
            f=self.ui
            for instr in self.list_of_all_comboboxes():
                cbb=eval("f."+instr)#get the pointer to the combobox
                add=eval("f."+instr.replace("instrtype","visa_address"))#get the pointer to the visa address box
                chb=eval("f."+instr.replace("instrtype","on"))#get the pointer to the check box
                savefile.write(instr.encode('utf8')+"\n")
                savefile.write(cbb.currentText().encode('utf8')+"\n") #instruments type
                savefile.write(add.text().encode('utf8')+"\n") #instr address
                savefile.write(str(chb.isChecked())+"\n") #instr is checked
            savefile.close()
        
    def loadInstrconf(self,fileName=None):
        if fileName==None:
            fileName = QFileDialog.getOpenFileName(self,"Load Configuration",directory= "./Configuration/Instruments",filter="Config file (*.cfg)")
            #PySide only
            #open() does not work with 'unicode' type object, conversion is needed
#            fileName=fileName[0].encode('utf8')
        if fileName!="":
            file_opened=open(fileName,'r')
            lines=file_opened.readlines()
            for i in range(len(lines)/4):
                instr=lines[4*i]
                instr_type=lines[4*i+1][:-1]
                visa_address=lines[4*i+2][:-1]
                instr_checked=lines[4*i+3][:-1]
                #update the interface
                f=self.ui
                cbb=eval("f."+instr)#get the pointer to the combobox
                add=eval("f."+instr.replace("instrtype","visa_address"))#get the pointer to the visa address box
                chb=eval("f."+instr.replace("instrtype","on"))#get the pointer to the check box
                index=cbb.findText(instr_type)
                if index<cbb.count():cbb.setCurrentIndex(index)
                add.setText(visa_address)
                if instr_checked=="True":
                    chb.setChecked(True)
                else:
                    chb.setChecked(False)

            file_opened.close()

    def loaddefaultconfig(self):
        try:
            self.loadInstrconf("./Configuration/Instruments/CurrentInstruments.cfg")
        except:
            pass

    def write2inst(self):
        address = self.ui.testinst.text()
        io = visa.ResourceManager().open_resource(address)
        command = self.ui.testcommand.text()
        with self.reserved_access_to_instr:
            io.write(command)
        
    def ask2inst(self):
        address = self.ui.testinst.text()
        io = visa.ResourceManager().open_resource(address)
        command = self.ui.testcommand.text()
        with self.reserved_access_to_instr:
            answer = io.query(command)
        self.ui.testanswer.setPlainText(answer)

    def readinst(self):
        address = self.ui.testinst.text()
        io = visa.ResourceManager().open_resource(address)
        with self.reserved_access_to_instr:
            answer = io.read_raw()
        self.ui.testanswer.setPlainText(answer)
        

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Instruments_connection(app,debug=True)
    window.show()
    sys.exit(app.exec_())

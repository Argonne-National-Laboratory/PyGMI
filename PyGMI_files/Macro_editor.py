import os,time
from PyQt4.QtGui import QWidget,QApplication,QSyntaxHighlighter,QTextCharFormat,QFont,QFileDialog,QStandardItemModel,QStandardItem
from PyQt4.QtCore import Qt,QTimer,QRegExp
from Macro_editor_Ui import Ui_Macro_editor

#Email capabilities
from measurements_done_alert import Email_alert,Email_one_file,Email_directory

################################################
#non capturing version of the regular expressions
#Regexfloat="(?:[-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)"
#Regexsimplefile="(?:[\w -\.]+)"
################################################
#capturing version of the regular expressions
Regexfloat="([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)"
Regexsimplefile="(\w+[\w -\./]*)"

################################################
#Regular expression for interpreting macro commands and capturing the parameters


class Macro_editor(QWidget):
    def __init__(self,parent=None,title='Macro editor'):
        # This class derivates from a Qt Widget so we have to call
        # the class builder ".__init__()"
        QWidget.__init__(self)
        # "self" is now a Qt Widget, then we instantiate the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = Ui_Macro_editor()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a reference to the Qt Widget where it will appear, i.e. itself
        # but the elements of the GUI will actually be children of the GUI (i.e of self.ui not of self)
        self.ui.setupUi(self)
        self.setWindowTitle(title)

        ### Dirty FIX: the macro editor is in a layout and a group box which somehow
        ### put it way down the list of children, so we need the 6th order parent of that to get to the main !
        ##self.main=self.parent().parent().parent().parent().parent().parent()
        ### FIXED:the main class now simply gives a link to itself when it instantiates the Macro Editor
        ### this has the added benefit of keeping track of which class may use the main
        self.main=parent
        self.macro_isActive=False

    def setupmain(self,main):
        # first called at startup by main program
        self.main = main

    def update_commands(self,meas_prog_list_byname):
        global Regexprogramfile
        Regexprogramfile="("+"|".join(meas_prog_list_byname)+")"
        self.valid_list_of_commands = self.get_list_of_commands()
        #initiate syntax highlighting for the macro editor
        self.highlighter = MacroHighlighter(self.ui.macro_textbox.document(),self.valid_list_of_commands)
        #update the list of available macro commands in the user interface
        model=QStandardItemModel()
        parentItem = model.invisibleRootItem()
        for command in self.valid_list_of_commands:
            parentItem.appendRow(QStandardItem(command.label))
        self.ui.macrocommandtree.setModel(model)

    def setuptimer(self):
        # second called at startup by main program
        self.valid_list_of_commands = self.get_list_of_commands()

        self.macro_timer = QTimer()
        #Use a single shot timer in between commands
        #otherwise it may fire again before the task is completed
        self.macro_timer.setSingleShot(True)
        self.macro_timer.timeout.connect(self.next_command)
                       


    def get_list_of_commands(self):        
        # List the Macro command that will be loaded and available
        # into the Macro editor.
        # Once you have created a new Macro command class in this file
        # you must add it in this list for it to be available in 
        # the Macro editor.
        # You may also remove commands from this list if you want to deactivate them
        return [
#           AngleCommand(),
            CommentsCommand(),
            WaitCommand(),
            WaitForEpoch(),
#            SetFieldCommand(),
#            WaitForHStableCommand(),
            WaitForMeasureCommand(),
#            SetPersistFieldCommand(),
#            SetTempCommand(),
#            SetHeaterCommand(),
#            WaitForTStableCommand(),
#            SetTempVTICommand(),
#            SetVTIHeaterCommand(),
            SetPPMSTempCommand(),
            SetPPMSFieldCommand(),
            WaitForTPPMSStableCommand(),
            WaitForHPPMSStableCommand(),
            SetSaveFileCommand(),
            StartMeasureCommand(),
            StopMeasureCommand(),
            EmailCommand(),
            EmailFileCommand(),
            EmailDirCommand(),
            SetICommand(),
            SetVCommand(),
            SetUICommand(self.main)]
                
    def save_macro(self):
        #the static method calls the native file system method
        fileName = QFileDialog.getSaveFileName(self,"Save Macro",directory= "./Macro",filter="Macro file (*.mac)")
        #open() does not work with 'unicode' type object, conversion is needed 
#        fileName=fileName[0].encode('utf8')
        if fileName!="":
            #get the macro text from frontpanel text box
            mac_unicode=self.ui.macro_textbox.toPlainText()
            #print fileName
            #(u'C:/Python27/Lib/site-packages/pyqtgraph/examples/test.txt', u'All Files (*.*)')
            #WARNING: write() and open() do not work with 'unicode' type object
            #they have to be converted to a string first (i.e. a list of bytes)
            savefile=open(fileName,'w')
            savefile.write(mac_unicode.encode('utf8'))
            savefile.close()
                
    def open_macro(self):
        fileName = QFileDialog.getOpenFileName(self,"Open Macro",directory= "./Macro",filter="Macro file (*.mac)")
        #open() does not work with 'unicode' type object, conversion is needed 
#        fileName=fileName[0].encode('utf8')
        if fileName!="":
            open_file=open(fileName,'r')
            self.ui.macro_textbox.setPlainText(unicode(open_file.read(-1),encoding='utf-8')) #'-1' to read the whole file at once
            open_file.close()

    def run_macro(self):
        if not(self.macro_isActive):
            self.macro_isActive=True
            self.current_macro=self.ui.macro_textbox.toPlainText().encode('utf8').split('\n')
            self.current_line=0
            self.cur_mac_max=len(self.current_macro)
            #single shot timer
            print "Starting Macro"
            self.macro_timer.start(0)
    
    def next_command(self):
        if self.current_line<self.cur_mac_max:
            #update the info line with the line being analyzed
            action=self.current_macro[self.current_line]
            self.ui.mac_curr_line.setText("line "+str(self.current_line)+": "+action)
            
            next_move=1
            wait_time=500
            for command in self.valid_list_of_commands:
                #run the command, if command matches the line being analyzed
                if command.regexp.indexIn(action)!=-1:
                    command.run(self.main)
                    next_move=command.next_move
                    wait_time=command.wait_time
                    break #break the for loop
            #go to line N+next_move of the current macro, after wait_time milliseconds
            self.current_line+=next_move
            self.macro_timer.start(wait_time)
        else:
            #end of macro reached
            self.stop_macro()
            
    def stop_macro(self):
        self.macro_timer.stop()
        self.macro_isActive=False
        #TODO : signal/slot !!!
        if self.main.measurements_thread.isAlive(): 
            self.main.stop_measurements()
        print "End of Macro"

    #for future update
    #def add_macroline(self,item,index):
        ##Open a short form to enter new parameters when a command line is double clicked
        #form=My_Form(form_string=item.text(0))
        ##print "entering the form"
        #if form.dialog_needed:
            #if form.exec_():
                #cursor=self.ui.macro_textbox.textCursor()
                #cursor.movePosition(cursor.StartOfBlock)
                #self.ui.macro_textbox.setTextCursor(cursor)
                #self.ui.macro_textbox.insertPlainText(form.user_string+'\n')
            ##print "returning from the form"
        #else:
            #cursor=self.ui.macro_textbox.textCursor()
            #cursor.movePosition(cursor.StartOfBlock)
            #self.ui.macro_textbox.setTextCursor(cursor)
            #self.ui.macro_textbox.insertPlainText(form.user_string+'\n')
            #form.done(1)
            ##print "no form was needed"

class New_command_template():
    def __init__(self):
        #Text that will appear in the list of commands on the right side of the Macro editor
        self.label=""
        #Regular expression which may or may not catch parameters
        self.regexp_str=""
        #Add this to the beginning and end of the regular expression
        #so that whitespaces before and after will not prevent the regex from matching
        self.regexp_str="^ *"+self.regexp_str+" *$"
        #instantiate regex
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        #what to do when the regex defined just above in __init__
        #has matched the current line of the Macro
        #get the captured parameters
        #values=self.regexp.capturedTexts()
        #send commands to instruments
        ##>change the temperature setpoint
        #with main.reserved_access_to_instr:
        #    main.temp_controller.switch_ramp(loop,'off')
        #    main.temp_controller.set_setpoint(loop,setpoint)
        #modify stuff in the interface
        ##>set the voltage
        #if values[1] in ['1','2','3']:
        #    V_source_setpoint=eval("main.ui.V_setpoint_"+values[1])
        #    V_source_setpoint.setValue(float(values[2]))
        #Finally go to next line of macro...
        self.next_move=1
        #...after 10 milliseconds
        self.wait_time=10 

class AngleCommand():
    def __init__(self):
        #Text that will appear in the list of commands on the right side of the Macro editor
        self.label="Set start|stop|step angle to FLOAT"
        #Regular expression which may or may not catch parameters
        self.regexp_str="Set (start|stop|step) angle to "+Regexfloat
        #Add this to the beginning and end of the regular expression
        #so that whitespaces before and after will not prevent the regex from matching
        self.regexp_str="^ *"+self.regexp_str+" *$"
        #instantiate regex
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        #what to do when the regex defined just above in __init__
        #has matched the current line of the Macro
        #get the captured parameters
        values=self.regexp.capturedTexts()
        #set the corresponding angle box
        if values[1] in ['stop','step','start']:
            anglebox=eval("main.ui.angle"+values[1])
            anglebox.setValue(float(values[2]))           
        #Finally go to next line of macro...
        self.next_move=1
        #...after 10 milliseconds
        self.wait_time=10 


class CommentsCommand():
    def __init__(self):
        self.regexp_str="""^##.*"""
        self.label="""## SOME COMMENTS"""
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        #go to next line of macro after 10 milliseconds
        self.next_move=1
        self.wait_time=10      
    
        
class WaitCommand():
    def __init__(self):
        self.regexp_str="Wait "+Regexfloat+" secs"
        self.label="Wait X secs"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #self.values[1]!=''
        #go to next line of macro after 'values[1]' seconds
        self.next_move=1
        self.wait_time=float(values[1])*1000      

class WaitForEpoch():
    def __init__(self):
        self.regexp_str="Wait for Epoch \+ "+Regexfloat+" secs"
        self.label="Wait for Epoch + X secs"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #test if the current time is greater than the time provided in the macro (in Epoch seconds)
        if float(values[1])>time.time():
            self.next_move=0
            self.wait_time=5000
        else:
            self.next_move=1
            self.wait_time=100

class SetFieldCommand():
    def __init__(self):
        self.regexp_str="Set Field of magnet (X|Y|Z) to "+Regexfloat+" G(?: @ "+Regexfloat+" G/s)?"
        self.label="Set Field of magnet X|Y|Z to X G (@ X G/s)"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        with main.reserved_access_to_instr:
            magnet=eval("main.magnet_"+values[1])
            if values[3]!='':
                #if a ramp rate was also provided, go to this setpoint at this rate
                magnet.program_ramp_rate_in_Gauss_per_second(float(values[3]))    
            #print "Setting Field to ",
            magnet.program_field_in_kG(float(values[2])*1e-3)
            magnet.ramp_to_programmed_field()
        #go to next line of macro
        self.next_move=1
        self.wait_time=500  
            
class WaitForHStableCommand():
    def __init__(self):
        self.regexp_str="Wait(?: at most "+Regexfloat+" secs)? for magnet (X|Y|Z) to finish ramping"
        self.label="Wait (at most X secs) for magnet (X|Y|Z) to finish ramping"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #wait for field to stabilize (and lock only when accessing the instrument)
        with main.reserved_access_to_instr:
            magnet=eval("main.magnet_"+values[2])
            stat=magnet.query_status()
        if self.waiting==False:
            self.waiting=True
            self.waiting_start=time.clock()
        if not(stat=='RAMPING to programmed current/field') or (values[1]!='' and time.clock()-self.waiting_start>float(values[1])):
            #ramping is finished or time limit is reached, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        else:
            #wait 5s and check again
            self.next_move=0
            self.wait_time=5000       
            
class WaitForMeasureCommand():
    def __init__(self):
        self.regexp_str="Wait(?: at most "+Regexfloat+" secs)? for measurements completion"
        self.label="Wait(at most X secs) for measurements completion"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        if self.waiting==False:
            self.waiting=True
            self.waiting_start=time.clock()
        if not(main.measurements_thread.isAlive()) or (values[1]!='' and time.clock()-self.waiting_start>float(values[1])):
            #Measurements are complete or time limit was reached, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        else:
            #wait 1s and check again if measurements are complete
            self.next_move=0
            self.wait_time=1000

class SetPersistFieldCommand():
    def __init__(self):
        self.regexp_str="Set persistent field in magnet (X|Y|Z) to "+Regexfloat+" T"
        self.label="Set persistent field in magnet X|Y|Z to x T"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
            
    def run(self,main):
        values=self.regexp.capturedTexts()
        ##set the loop index and setpoint value
        magnet_setpoint=eval("main.ui.B_"+values[1]+"_setpoint")
        magnet_setpoint.setValue(float(values[2]))
        time.sleep(1)
        main.ui.measMode.setCurrentIndex(main.ui.measMode.findText("Change_persistent_"+values[1]+"_field"))
        #start measurements
        main.start_measurements()     
        #go to next line of macro after stdwtime (give some time to process other events)
        self.next_move=1
        self.wait_time=500


class SetPPMSTempCommand():
    def __init__(self):
        self.regexp_str="Set PPMS Temperature to "+Regexfloat+" K @ "+Regexfloat+" K/min (FastSettle|NoOvershoot)?"
        self.label="Set PPMS Temperature to X K @ X K/min (FastSettle/NoOvershoot)"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        ##get the loop index and setpoint value
        setpoint=float(values[1])
        rate=float(values[2])
        #if an approach was also provided, go to this setpoint at this rate
        approach = 'FastSettle'      
        if values[3]!='':approach = values[3]
        with main.reserved_access_to_instr:
            main.ppms.set_temperature(setpoint,rate,approach)
        
        #go to next line of macro after stdwtime (give some time to process other events)
        self.next_move=1
        self.wait_time=100

class SetPPMSFieldCommand():
    def __init__(self):
        self.regexp_str="Set PPMS Field to "+Regexfloat+" Oe @ "+Regexfloat+" Oe/s (Linear|NoOvershoot|Oscillate)? (Persistent|Driven)?"
        self.label="Set PPMS Field to X Oe @ X Oe/s (Linear|NoOvershoot|Oscillate) (Persistent|Driven)"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        ##get the loop index and setpoint value
        setpoint=float(values[1])
        rate=float(values[2])
        #if an approach was also provided, go to this setpoint at this rate
        approach = 'Linear'
        mode = 'Persistent'
        if values[3]!='':approach = values[3]
        if values[4]!='':mode = values[4]
        with main.reserved_access_to_instr:
            main.ppms.set_field(setpoint,rate,approach,mode)
        
        #go to next line of macro after stdwtime (give some time to process other events)
        self.next_move=1
        self.wait_time=100

class WaitForHPPMSStableCommand():
    def __init__(self):
        self.regexp_str="Wait(?: at most "+Regexfloat+" secs)? for PPMS Field to reach "+Regexfloat+" Oe"
        self.label="Wait(at most X secs) for PPMS Field to reach X Oe"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #Wait for the field to be stable and
        #within 5% of specified field
        #(and lock only when accessing the instrument)
        with main.reserved_access_to_instr:
            Herror, H, status = main.ppms.get_field()
        if self.waiting==False:
            self.waiting=True
            self.waiting_start=time.clock()
        if 'Stable' in status and (abs(H-float(values[2]))<abs(float(values[2])*0.05) or abs(H-float(values[2]))<1.0):
            #Field is stable, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        elif values[1]!='' and time.clock()-self.waiting_start>float(values[1]):
            #time limit is reached, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        else:
            #wait 10s and check again
            self.next_move=0
            self.wait_time=10000 
                                    
class SetTempCommand():
    def __init__(self):
        self.regexp_str="Set Loop (\d+) to "+Regexfloat+" K(?: @ "+Regexfloat+" K/min)?"
        self.label="Set Loop X to X K (@ X K/min)"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        ##get the loop index and setpoint value
        loop=float(values[1])
        setpoint=float(values[2])
        #if a ramp rate was also provided, go to this setpoint at this rate
        if values[3]!='':
            rate=float(values[3])
            with main.reserved_access_to_instr:
                main.temp_controller.conf_ramp(loop,rate,'on')
                main.temp_controller.set_setpoint(loop,setpoint)
        else:        
            with main.reserved_access_to_instr:            
                main.temp_controller.switch_ramp(loop,'off')
                main.temp_controller.set_setpoint(loop,setpoint)
        #go to next line of macro after stdwtime (give some time to process other events)
        self.next_move=1
        self.wait_time=500


class SetHeaterCommand():
    def __init__(self):
        self.regexp_str="Set heater range to (\d)"
        self.label="Set heater range to DIGIT"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #set the heater range
        with main.reserved_access_to_instr:
            main.temp_controller.set_heater_range(int(values[1]))
        #go to next line of macro
        self.next_move=1
        self.wait_time=500   

class WaitForTPPMSStableCommand():
    def __init__(self):
        self.regexp_str="Wait(?: at most "+Regexfloat+" secs)? for PPMS Temp to reach "+Regexfloat+" K"
        self.label="Wait(at most X secs) for PPMS Temp to reach X K"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #Wait for the temperature measurement to be stable and
        #within 5% of specified temperature
        #(and lock only when accessing the instrument)
        with main.reserved_access_to_instr:
            Terror, T, status = main.ppms.get_temperature()
        if self.waiting==False:
            self.waiting=True
            self.waiting_start=time.clock()
        if status == 'Stable' and abs(T-float(values[2]))<abs(float(values[2])*0.05):
            #Temperature is stable, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        elif values[1]!='' and time.clock()-self.waiting_start>float(values[1]):
            #time limit is reached, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        else:
            #wait 10s and check again
            self.next_move=0
            self.wait_time=10000 
            
class WaitForTStableCommand():
    def __init__(self):
        self.regexp_str="Wait(?: at most "+Regexfloat+" secs)? for channel (\w) to reach "+Regexfloat+" \+/\- "+Regexfloat+" K"
        self.label="Wait(at most X secs) for channel X to reach X +/- X K"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #wait for temperature to stabilize (and lock only when accessing the instrument)
        with main.reserved_access_to_instr:
            T=main.temp_controller.query_temp(values[2])
        if self.waiting==False:
            self.waitTcounter=0
            self.waiting=True
            self.waiting_start=time.clock()
        if values[1]!='' and time.clock()-self.waiting_start>float(values[1]):
            #time limit is reached, go to next line of macro
            self.waiting=False
            self.next_move=1
            self.wait_time=500
        elif abs(T-float(values[3]))<float(values[4]):
            #Wait for the temperature measurement to be ten times
            #within the specified limits, in a row, to consider it stable
            if self.waitTcounter<10:
                #count one, wait 0.5 secs and measure T again
                self.waitTcounter+=1
                self.next_move=0
                self.wait_time=500
            else:
                #Temperature is stable, go to next line of macro
                self.waitTcounter=0
                self.waiting=False
                self.next_move=1
                self.wait_time=500                
        else:
            #wait 10s and check again, but reset the stable temperature counter
            self.waitTcounter=0
            self.next_move=0
            self.wait_time=10000 


class SetTempVTICommand():
    def __init__(self):
        self.regexp_str="Set VTI Loop (\d+) to "+Regexfloat+" K(?: @ "+Regexfloat+" K/min)?"
        self.label="Set VTI Loop X to X K (@ X K/min)"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
        self.waiting=False
        self.waiting_start=0
        
    def run(self,main):
        values=self.regexp.capturedTexts()
        ##get the loop index and setpoint value
        loop=float(values[1])
        setpoint=float(values[2])
        #if a ramp rate was also provided, go to this setpoint at this rate
        VTI=main.instr_9
        if values[3]!='':
            rate=float(values[3])
            with main.reserved_access_to_instr:
                VTI.conf_ramp(loop,rate,'on')
                VTI.set_setpoint(loop,setpoint)
        else:        
            with main.reserved_access_to_instr:            
                VTI.switch_ramp(loop,'off')
                VTI.set_setpoint(loop,setpoint)
        #go to next line of macro after stdwtime (give some time to process other events)
        self.next_move=1
        self.wait_time=500
        

class SetVTIHeaterCommand():
    def __init__(self):
        self.regexp_str="Set VTI heater range to (\d)"
        self.label="Set VTI heater range to DIGIT"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #set the heater range
        with main.reserved_access_to_instr:
            main.instr_9.set_heater_range(int(values[1]))                     
        #go to next line of macro
        self.next_move=1
        self.wait_time=500         
                
                             
class SetSaveFileCommand():
    def __init__(self):
        self.regexp_str="Set Save file to "+Regexsimplefile+""
        self.label="Set Save file to X"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        main.ui.savefile_txt_input.setText(values[1])
        #new file name is set, go to next line of macro
        self.next_move=1
        self.wait_time=500                                     
                    
        
class StartMeasureCommand():
    def __init__(self):
        #type name_of_program() to start it
        self.regexp_str="Start "+Regexprogramfile+"\((.*)\)"
        self.label="Start PROGRAM()"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        main.ui.measMode.setCurrentIndex(main.ui.measMode.findText(values[1]))
        #start measurements
        main.start_measurements()
        #go to next line of macro
        self.next_move=1
        self.wait_time=500                      

        
class StopMeasureCommand():
    def __init__(self):
        self.regexp_str="Stop Measurements"
        self.label="Stop Measurements"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        main.stop_measurements()
        #go to next line of macro
        self.next_move=1
        self.wait_time=500                                     
            
            
class EmailCommand():
    def __init__(self):
        self.regexp_str="E-mail message: "+Regexsimplefile
        self.label="E-mail message: MESSAGE"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        msg=values[1]
        try:
            email_alert=Email_alert(message=msg.encode('utf8'),address=main.ui.email_address.text(),subject="Message from PyGMI",smtpadd=main.mainconf['smtpadd'],login=main.mainconf['login'],mdp=main.mainconf['mdp'],smtpport=main.mainconf['smtpport'])
            print "message successfully sent by e-mail"
        except:
            print "Exception: message could not be sent by e-mail"
        #go to next line of macro
        self.next_move=1
        self.wait_time=500   
 
 
class EmailFileCommand():
    def __init__(self):
        self.regexp_str="E-mail file: "+Regexsimplefile
        self.label="E-mail file: FILE"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        file_path=values[1]
        try:
            message="Hi,\n\nat your request, here is the file :"+os.path.normpath(os.path.abspath(file_path.encode('utf8').strip()))+"\n\n PyGMI"
            email_alert=Email_one_file(one_file=file_path.encode('utf8').strip(),address=main.ui.email_address.text(),message=message,subject="Data file from PyGMI",smtpadd=main.mainconf['smtpadd'],login=main.mainconf['login'],mdp=main.mainconf['mdp'],smtpport=main.mainconf['smtpport'])
            print "file successfully sent by e-mail"
        except:
            print "Exception: file could not be sent by e-mail"
        #go to next line of macro
        self.next_move=1
        self.wait_time=500   


class EmailDirCommand():
    def __init__(self):
        self.regexp_str="E-mail directory: "+Regexsimplefile
        self.label="E-mail directory: DIRECTORY"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        dir_path=values[1]
        try:
            message="Hi,\n\nat your request, here is the directory: "+os.path.normpath(os.path.abspath(dir_path.encode('utf8').strip()))+"\n\n PyGMI"
            email_alert=Email_directory(directory=dir_path.encode('utf8').strip(),address=main.ui.email_address.text(),message=message,subject="Data directory from PyGMI",smtpadd=main.mainconf['smtpadd'],login=main.mainconf['login'],mdp=main.mainconf['mdp'],smtpport=main.mainconf['smtpport'])
            print  "directory successfully sent by e-mail"
        except:
            print "Exception: directory could not be sent by e-mail"
        #go to next line of macro
        self.next_move=1
        self.wait_time=500   


class SetUICommand():
    def __init__(self,main):
#        print "|".join(dir(main.ui))
        self.regexp_str="Set UI ("+"|".join(dir(main.ui))+") to "+Regexfloat
        self.label="Set UI PROPERTY to FLOAT"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #set the property
        prop = eval("main.ui."+values[1])
        prop.setValue(float(values[2]))
        #go to next line of macro
        self.next_move=1
        self.wait_time=10
    

class SetICommand():
    def __init__(self):
        self.regexp_str="Set current (\d) to "+Regexfloat+" A"
        self.label="Set current DIGIT to FLOAT A"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #set the current
        if values[1]=='1':
            main.ui.I_source_setpoint.setValue(float(values[2])*1e6)
        elif values[1] in ['2','3']:
            I_source_setpoint=eval("main.ui.I_source_setpoint_"+values[1])
            I_source_setpoint.setValue(float(values[2])*1e6)
        #go to next line of macro
        self.next_move=1
        self.wait_time=10


class SetVCommand():
    def __init__(self):
        self.regexp_str="Set voltage (\d) to "+Regexfloat+" V"
        self.label="Set voltage DIGIT to FLOAT V"
        self.regexp_str="^ *"+self.regexp_str+" *$" #so that the same string with heading and trailing whitespaces also matches
        self.regexp=QRegExp(self.regexp_str)
    
    def run(self,main):
        values=self.regexp.capturedTexts()
        #set the voltage
        if values[1] in ['1','2','3']:
            V_source_setpoint=eval("main.ui.V_setpoint_"+values[1])
            V_source_setpoint.setValue(float(values[2]))
        #go to next line of macro
        self.next_move=1
        self.wait_time=500
  
                 

class MacroHighlighter(QSyntaxHighlighter):
    def __init__(self,textboxdoc,valid_list_of_commands):
        QSyntaxHighlighter.__init__(self,textboxdoc)
        self.valid_syntax="|".join([command.regexp_str for command in valid_list_of_commands])
        self.my_expression = QRegExp(self.valid_syntax)
        #define a blue font format for valid commands
        self.valid = QTextCharFormat()
        self.valid.setForeground(Qt.black)
        #define a bold red font format for invalid commands
        self.invalid = QTextCharFormat()
        self.invalid.setFontWeight(QFont.Bold)
        self.invalid.setForeground(Qt.red)
        #define a blue font format for valid parameters
        self.valid_value=QTextCharFormat()        
        self.valid_value.setFontWeight(QFont.Bold)
        #self.valid_value.setForeground(QColor.fromRgb(255,85,0))
        self.valid_value.setForeground(Qt.blue)
                
    def highlightBlock(self, text):
        #this function is automatically called when some text is changed
        #in the texbox. 'text' is the line of text where the change occured    
        #check if the line of text contains a valid command
        match = self.my_expression.exactMatch(text)
        if match:
            #valid command found: highlight the command in blue
            self.setFormat(0, len(text), self.valid)
            #highlight the parameters in orange
            #loop on all the parameters that can be captured
            for i in range(self.my_expression.captureCount()):
                #if a parameter was captured, it's position in the text will be >=0 and its capture contains some value 'xxx'
                #otherwise its position is -1 and its capture contains an empty string ''
                if self.my_expression.pos(i+1)!=-1:
                    self.setFormat(self.my_expression.pos(i+1), len(self.my_expression.cap(i+1)), self.valid_value)
        else:
            #no valid command found: highlight in red
            self.setFormat(0, len(text), self.invalid)



#################################
##  NB:MyMacroEdit cannot be included in this file because it will make a circular reference
##  indeed Macro_editor will try to import Macro_editor_Ui which will try to import MyMacroEdit from MacroEditor
                
if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Macro_editor(app)
    window.setupmain(None)
    import Measurements_programs
    window.update_commands(Measurements_programs.__all__)
    window.setuptimer()
    window.show()
    sys.exit(app.exec_())

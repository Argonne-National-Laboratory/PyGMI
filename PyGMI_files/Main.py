# -*- coding: utf-8 -*-
#Libraries Imports
#Time measurements
import time
#Multithreading
import threading
import Queue
#User interface
    ##PyQt4
from PyQt4.QtGui import QMainWindow,QFileDialog
from PyQt4.QtCore import QTimer,SIGNAL
    ##Main user interface
import GUI_compiled
    ##Widgets that may be created as independent windows
from Plot2DDataWidget import Plot2DDataWidget
from Config_menu import Config_menu
    ##Retriever of all values of the front panel
from Frontpanel_values import Frontpanel_values
#User written Measurements Programs
import Measurements_programs
for module in Measurements_programs.__all__:
    exec('import Measurements_programs.'+module)

class start_GUI(QMainWindow):
    def __init__(self):
        # This class derivates from a Qt MainWindow so we have to call
        # the class builder ".__init__()"
        QMainWindow.__init__(self)
        # "self" is now a Qt Mainwindow, then we load the user interface
        # generated with QtDesigner and call it self.ui
        self.ui = GUI_compiled.Ui_PyGMI()
        # Now we have to feed the GUI building method of this object (self.ui)
        # with a Qt Mainwindow, but the widgets will actually be built as children
        # of this object (self.ui)
        self.measdata=[[1,3,2],[3,5,7]]
        self.current_header=["index","prime numbers"]
        self.ui.setupUi(self)
        # initialize a QTimer for periodic data transfer with the measuring thread
        self.save_data_timer = QTimer()
        self.save_data_timer.setSingleShot(True)
        self.save_data_timer.timeout.connect(self.save_data)
        # initialize a Queue to retrieve data from the measuring thread
        self.data_queue=Queue.Queue()
        self.measurements_thread_stop_flag=threading.Event()
        self.measurements_thread=threading.Thread()
        # initialize a Lock to reserve access to the instruments
        self.reserved_access_to_instr=threading.Lock()
        #initiate a flag to wait for a parameter to settle
        self.waiting=False
        #give the reference "self" (the main thread) to the Macro Editor
        # and set-up its list of available measurements programs to run
        self.ui.macro_UI.setupmain(self)
        # initiate the list of available measurements program
        # AND update the macro editor with the list of programs available
        self.update_list_of_meas_program()
        # finish macro initialization
        self.ui.macro_UI.setuptimer()

        #initialize a list that will retain a reference to the independent plot windows
        self.plotwindows=[]
        #give the reference "self" (the main thread) to the fixed plot windows
        self.ui.Plot2D_1.parent=self
        self.ui.Plot2D_2.parent=self
        self.ui.Plot2D_3.parent=self
        self.ui.Plot2D_4.parent=self
        #give the reference "self" (the main thread) to the Instruments connector
        self.ui.instr_IO.parent=self
        self.ui.instr_IO.set_up_instr_access_lock(self.reserved_access_to_instr)
        self.ui.instr_IO.loaddefaultconfig()

        
        self.mainconf={}
        self.loaddefaultconfig()
   
    def fixed_plot_conf(self):
        for plot in [self.ui.Plot2D_1,self.ui.Plot2D_2,self.ui.Plot2D_3,self.ui.Plot2D_4]:
            plot.parent=self
            plot.change_line_color(self.mainconf['linecolor'])
            plot.change_point_color(self.mainconf['pointcolor'])
            plot.change_symbol_size(self.mainconf['pointsize'])
        
    def update_list_of_meas_program(self):
        """update the list of available measurements program and recompile them"""
        self.meas_thread_list=[]
        # used for Macro_editor so that the command that start programs, knows which are available
        self.meas_prog_list_byname = []
        self.ui.measMode.clear()
        already_imported=Measurements_programs.__all__
        reload(Measurements_programs)
        for module in Measurements_programs.__all__:
            if module in already_imported:
                exec('reload(Measurements_programs.'+module+')')
            else:
                exec('import Measurements_programs.'+module)
            exec('Meas_script=Measurements_programs.'+module+'.Script')
            self.meas_thread_list.append(Meas_script)
            self.ui.measMode.addItem(module)
            self.meas_prog_list_byname.append(module)
        # update the macro editor with the new list of available programs to run
        self.ui.macro_UI.update_commands(self.meas_prog_list_byname)
        print "List of Programs Updated" 

    def create_new_plotwidget(self):
        #print "creating new plot widget"
        newwindow=Plot2DDataWidget(self,self.measdata,self.current_header,SymbolSize=self.mainconf['pointsize'],linecolor=self.mainconf['linecolor'],pointcolor=self.mainconf['pointcolor'],title=self.ui.NewPlotWindowTitle.text())
        #a reference to the window must be kept, otherwise the new window is immediately garbage collected !
        self.plotwindows.append(newwindow)
        newwindow.show()
        
    def loaddefaultconfig(self):
        window = Config_menu(self,config_dict=self.mainconf)
        window.update_values()

    def create_config_menu(self):
        newwindow=Config_menu(self,config_dict=self.mainconf)
        #a reference to the window must be kept, otherwise the new window is immediately garbage collected !
        self.plotwindows.append(newwindow)
        newwindow.show()

    def save_data(self):
        """function called periodically by a timer to check if some data
        was put by the measurements thread in the "queue" (buffer),
        and, if so, update the Master dataset "self.measdata" and save
        it to the disk"""
        while not(self.data_queue.empty()):
            #NB:Queues are thread-safe: they won't be accessed by several threads at the same time
            #the lock mechanism is automatically included within them
            #block=False: means do not block execution until some data is put in the queue
            data,note=self.data_queue.get(block=False)
            #the measuring thread may send three different types of
            #information through the Queue, "note" indicates which type it is
            if note=='newfile':
                #close previous file and open a new one
                self.savefile.close()
                try:
                    #write buffer to disk every 256 bytes of data (0.25 Ko)
                    self.savefile=open(data,'a',256)
                except:
                    try:
                        #save data even if the savefile could not be created (the name of which was provided by the user)
                        self.savefile=open("Unsaved-data-"+time.strftime("%a-%d-%b-%Y-%H-%M-%S-UTC", time.gmtime())+".txt",'a',256)
                    except:
                        self.savefile=open("Savefile_of_last_resort",'a',256)
            elif note==True:
                #if note==True, "data" is actually a header for the incoming data
                ######initialize data storage######
                self.current_header=data
                #set-up empty data lists
                self.measdata=[ [] for i in range(len(data))]
                #######Store header to file#######
                self.savefile.write("\t".join(data)+'\n')
            else:
                #good data incoming (hopefully)
                #######Store data to file#########                
                self.savefile.write('\t'.join(map(str,data))+'\n')
                #######Update Master data list####
                for i in range(len(data)):
                    self.measdata[i].append(data[i])
            self.data_queue.task_done()
        self.save_data_timer.start(100)
           
    def switch_measurements_state(self):
        if self.measurements_thread.isAlive():
            self.stop_measurements()
        else:
            self.start_measurements()
    
    def start_measurements(self):
        #fetch the values from the frontpanel
        self.frontpanel_values=Frontpanel_values(self.ui)
        #print "Frontpanel loaded"
        #fetch the measurement type
        meas_thread_class=self.meas_thread_list[self.ui.measMode.currentIndex()]
        #print "Measurements prog loaded"
        ######initialize savefile######
        #it could be done in 'save_data' function, but then you mustn't access 
        #self.frontpanel, because the measurement thread has started, so just do it before starting the measurement thread 
        #256 is the buffer size in bytes, 'a' is for 'append', in order to ensure never to erase any file
        self.savefile=open(self.frontpanel_values.savefile_txt_input,'a',256)
        #initiate a thread to run the measurements without freezing the frontpanel
        #print "launching meas prog"
        self.measurements_thread=meas_thread_class(self,
                                                   self.frontpanel_values,
                                                   self.data_queue,
                                                   self.measurements_thread_stop_flag,
                                                   self.reserved_access_to_instr)
                                                   #self.instr_IO.connected_instr) for next upgrade
        #change the text on the button
        self.ui.pushButton.setText("Stop\nMeasurements")
        #start the measurements thread, which will run independently from the main thread
        self.measurements_thread.start()
        print "Measurements started"
        #start the timer that periodically saves the data
        self.save_data_timer.start(100)
        #initialize a QTimer to check measurement thread activity
        #and do the clean up when the measurement thread stops
        self.check_thread_activity = QTimer()
        self.check_thread_activity.timeout.connect(self.check_measurements)
        self.check_thread_activity.start(200)
    
    def check_measurements(self):
        if not(self.measurements_thread.isAlive()):
            self.stop_measurements()
        
    def stop_measurements(self):
        self.check_thread_activity.stop()
        if self.measurements_thread.isAlive():
            print "Stopping Measurements Thread"
            #tell the measurements thread to stop by setting this flag
            #(this flag is thread safe: it can't be access by both threads at the same time)
            self.measurements_thread_stop_flag.set()
            #wait for the thread to finish safely (it can take a while if the measurement program has few stopping points set up)
            self.measurements_thread.join()
            print "Measurements Thread Stopped"
        #reset the flag
        self.measurements_thread_stop_flag.clear()
        #stop the timer that saves data
        if self.save_data_timer.isActive():
            #abort the waiting time and immediateley finish saving data
            self.save_data_timer.stop()
            self.save_data()
            #previous line will relaunch the timer so stop it again
            self.save_data_timer.stop()
            self.savefile.close()
        #change the text on the button
        self.ui.pushButton.setText("Start\nMeasurements")
   
    def savefile_txt_input_open(self):
        fileName = QFileDialog.getSaveFileName(self,"Savefile",directory= "./measurements data")
        #if the user chooses 'Cancel' in the dialog, a unicode empty string is returned
#        if not(fileName[0]==u''):
        self.ui.savefile_txt_input.setText(fileName)

#Multithreading
import threading
#Time measurement
import time

######create a separate thread to run the measurements without freezing the front panel######
class Script(threading.Thread):
    def __init__(self,mainapp,frontpanel,data_queue,stop_flag,GPIB_bus_lock,**kwargs):
        #nothing to modify here
        threading.Thread.__init__(self,**kwargs)
        self.mainapp=mainapp
        self.frontpanel=frontpanel
        self.data_queue=data_queue
        self.stop_flag=stop_flag
        self.GPIB_bus_lock=GPIB_bus_lock
        
    def run(self):
        #this is the part that will be run in a separate thread
        #######################################################
        #SHORTCUTS
        instr=self.mainapp                             #a shortcut to the main app, especially the instruments
        f=self.frontpanel                          #a shortcut to frontpanel values
        reserved_bus_access=self.GPIB_bus_lock     #a lock that reserves the access to the GPIB bus
        #data_queue=self.data_queue  #a shortcut to a FIFO queue to send the data to the main thread
        #######################################################
        #SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"
        header=['Time (s)','H (T)']

        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,True))
        
        #######################################################
        #INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        
        magnet=instr.magnet_Z
                        
        #Instruments set-up
        with reserved_bus_access:
            magnet.set_field_in_Tesla(f.B_Z_setpoint)
            print "magnet status :",magnet.query_status()
            print "persistent switch status :",magnet.query_persistent_switch_state()
            print "persistent field in magnet :",magnet.last_known_field_value_in_T,"T"
            print "current programmed field :",magnet.query_programmed_field()
            print "current programmed ramp rate :",magnet.query_ramp_rate()
        ######Compile the latest data######
        t=time.clock()-start_time
        last_data=[t,magnet.last_known_field_value_in_T]
        #######Send the latest data to the main thread for display and storage######
        self.data_queue.put((last_data,False))

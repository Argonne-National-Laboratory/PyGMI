#Multithreading
import threading
#Time measurement
import time
#import numpy as np

######create a separate thread to run the measurements without freezing the front panel######
class Script(threading.Thread):
    def __init__(self,mainapp,frontpanel,data_queue,stop_flag,Instr_bus_lock,**kwargs):
        #nothing to modify here
        threading.Thread.__init__(self,**kwargs)
        self.mainapp=mainapp
        self.frontpanel=frontpanel
        self.data_queue=data_queue
        self.stop_flag=stop_flag
        self.Instr_bus_lock=Instr_bus_lock

    def run(self):
        #this is the part that will be run in a separate thread
        #######################################################
        #SHORTCUTS
        instr=self.mainapp                         #a shortcut to the main app, especially the instruments
        f=self.frontpanel                          #a shortcut to frontpanel values
#        reserved_bus_access=self.Instr_bus_lock     #a lock that reserves the access to instruments
        #data_queue=self.data_queue                #a shortcut to a FIFO queue to send the data to the main thread
        #######################################################
        #SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"

        header=['Time (s)','Time since Epoch']
#        header+=["Temperature (K)"]
        header+=["R (Ohm)","X (Ohm)"]
        header+=["Delay (s)"]
#        header+=["Excitation (A)"]
#        header+=["H (Oe)"]

        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,'header'))

        #######################################################
        #INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        LS = instr.instr_1
        # 40 ms delay seems optimal to avoid repeated points
        LS.delay = 40e-3
        #######################################################
        #MAIN LOOP
        time.sleep(2)
        while True:
#            if LS.delay>0:LS.delay-=1e-3
            #Check if the main process is telling to stop
            if self.stop_flag.isSet():
                break
            R = LS.query_R(4)
            X = LS.query_X(4)
            ######Compile the latest data######
            t = time.clock()-start_time
            epochtime = time.time()
            last_data = [t,epochtime]
            last_data.append(R)
            last_data += [X]
            last_data += [LS.delay]

            #######Send latest data to the main process for display and storage######
            self.data_queue.put((last_data,'data'))
            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)


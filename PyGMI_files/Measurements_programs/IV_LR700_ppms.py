#Multithreading
import threading
#Time measurement
import time
import numpy as np

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
        reserved_bus_access=self.Instr_bus_lock     #a lock that reserves the access to instruments
        #data_queue=self.data_queue                #a shortcut to a FIFO queue to send the data to the main thread
        #######################################################
        #SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"

        header=['Time (s)','Time since Epoch']
        header+=["Temperature (K)"]
        header+=["H (Oe)"]
        header+=["R (Ohm)","X (Ohm)"]
        header+=["Excitation (V)","I (A)"]


        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,'header'))

        #######################################################
        #INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        #I_source=instr.instr_8


        ppms = instr.ppms
        LR700 = instr.instr_1

        #Instruments set-up
        with reserved_bus_access:
            LR700.set_time_cste(10.0)
        #######################################################
        #MAIN LOOP
        for V in np.arange(f.current1,f.current2,f.current3):
            #Check if the main process is telling to stop
            if self.stop_flag.isSet():
                break
            for i in range(f.repeat_points):
                if self.stop_flag.isSet():
                    break
                with reserved_bus_access:
                    LR700.set_varexcitation(V)
                    Herror, Hexp, status = ppms.get_field()
                    time.sleep(0.1)
                    T = ppms.get_temperature()[1]
                    # the bridge needs 5s + filter TC to settle after a step
                    # change
                    time.sleep(15)
                    R = LR700.query_R()
                    X = LR700.query_X()
                    I = LR700.query_bridge_current()
                ######Compile the latest data######
                t=time.clock()-start_time
                epochtime=time.time()
                last_data=[t,epochtime]
                last_data.append(T)
                last_data+=[Hexp]
                last_data+=[R,X]
                last_data+=[V,I]


                #print last_data
                #print map(type,last_data)
                #######Send latest data to the main process for display and storage######
                self.data_queue.put((last_data,'data'))
                #######Wait mesure_delay secs before taking next measurements
                time.sleep(f.mesure_delay)


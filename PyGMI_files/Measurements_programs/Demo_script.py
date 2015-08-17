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
        m=self.mainapp              #a shortcut to the main app, especially the instruments
        f=self.frontpanel           #a shortcut to frontpanel values
        reserved_bus_access=self.GPIB_bus_lock     #a lock that reserves the access to the GPIB bus
        #data_queue=self.data_queue  #a shortcut to a FIFO queue to send the data to the main thread
        #######################################################
        #SAVEFILE HEADER - add column names to this list in the same order
        #as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way :
        #"self.data_queue.put(([some time, some current, some voltage],False))"
        header=['Time (s)']
        header+=['Time (min)']
        if f.temp_controller_on:header+=["T (K)"]
        if f.instr_on_1:header+=["Radius (V)","theta"]
        
        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,True))

        if f.instr_on_1:m.instr_1.set_amplitude(f.voltage1)
        
        #######Control parameters loop(s)######
        while True:
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break
            #reserve the access to the instruments, then discuss with them
            with reserved_bus_access:
                #Measure T
                if f.temp_controller_on:T=m.temp_controller.query_temp('B')
                #Measure R and theta
                if f.instr_on_1:freq,R1,theta1=m.instr_1.query_f_R_theta()
                #Measure R and theta
                if f.instr_on_1:freq,R2,theta2=m.instr_1.query_f_R_theta()
            R=(R1+R2)/2.0
            theta=(theta1+theta2)/2.0
            ######Compile the latest data######
            t=time.clock()-start_time
            last_data=[t,t/60.0]
            if f.temp_controller_on:last_data.append(T)
            if f.instr_on_1:last_data.extend([R,theta])
                            
            #######Send the latest data to the main thread for automatic display and storage into the savefile######
            self.data_queue.put((last_data,False))
            
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break            
            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)
        

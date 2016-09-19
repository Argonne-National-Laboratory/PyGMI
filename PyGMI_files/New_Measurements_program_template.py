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
        #SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"
        header=['Time (s)']
        if f.Temp_on:header+=["T (K)"]
        if f.magnet_on:header+=["H (G)"]
        if f.instr_on_1:header+=["I1"]
        if f.instr_on_2:header+=["p1","m1","V1"]
        if f.instr_on_3:header+=["I2"]
        if f.instr_on_4:header+=["p2","m2","V2"]
        if f.instr_on_5:header+=["I3"]
        if f.instr_on_6:header+=["p3","m3","V3"]
        if f.instr_on_7:header+=["I4"]
        if f.instr_on_8:header+=["p4","m4","V4"]
        if f.instr_on_9:header+=["I5"]
        if f.instr_on_10:header+=["p5","m5","V5"]
        if f.instr_on_11:header+=["I6"]
        if f.instr_on_12:header+=["p6","m6","V6"]
        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,True))
        
        #######Control parameters loop(s)######
        while True:
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break
            #reserve the access to the instruments, then discuss with them
            with reserved_bus_access:
                #Measure T,H
                if f.Temp_on:T=temp_controller.query_temp(f.temp_controller_channel)
                if f.magnet_on:H=magnet.query_programmed_field()
                
                #Measure with +I
                if f.instr1_on:
                    m.instr1.set_current_source_amplitude(f.current1)
                    time.sleep(0.05)
                if f.instr2_on:Vp1=instr2.query_voltage()
                #Measure with -I
                if f.instr1_on:
                    m.instr1.set_current_source_amplitude(-f.current1)
                    time.sleep(0.05)
                if f.instr2_on:Vm1=instr2.query_voltage()
                m.instr1.set_current_source_amplitude(0)
                
                #Measure with +I
                if f.instr3_on:
                    m.instr3.set_current_source_amplitude(f.current2)
                    time.sleep(0.05)
                if f.instr4_on:Vp2=m.instr4.query_voltage()
                #Measure with -I
                if f.instr3_on:
                    m.instr3.set_current_source_amplitude(-f.current2)
                    time.sleep(0.05)
                if f.instr4_on:Vm2=m.instr4.query_voltage()
                m.instr3.set_current_source_amplitude(0)
                
                #Measure with +I
                if f.instr5_on:
                    m.instr5.set_current_source_amplitude(f.current3)
                    time.sleep(0.05)
                if f.instr6_on:Vp3=m.instr6.query_voltage()
                #Measure with -I
                if f.instr5_on:
                    m.instr5.set_current_source_amplitude(-f.current3)
                    time.sleep(0.05)
                if f.instr6_on:Vm3=m.instr6.query_voltage()
                m.instr5.set_current_source_amplitude(0)
            
            ######Compile the latest data######
            t=time.clock()-start_time
            last_data=[t]
            if f.Temp_on:last_data.append(T)
            if f.magnet_on:last_data.append(H)
            if f.instr1_on:last_data.extend([f.current1,Vp1,Vm1,(Vp1-Vm1)/2.0])
            if f.instr3_on:last_data.extend([f.current2,Vp2,Vm2,(Vp2-Vm2)/2.0])
            if f.instr5_on:last_data.extend([f.current3,Vp3,Vm3,(Vp3-Vm3)/2.0])
            #if f.instr4_on:last_data.extend([Vp4,Vm4,(Vp4-Vm4)/2.0])
                
            #######Send the latest data to the main thread for automatic display and storage into the savefile######
            self.data_queue.put((last_data,False))
            
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break
            
            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)
        

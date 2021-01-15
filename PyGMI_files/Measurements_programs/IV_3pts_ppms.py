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
#        header+=["VpHall","VmHall","(VpHall-VmHall)/2"]
        header+=["VpR","VmR","(VpR-VmR)/2"]
        header+=["I (A)"]
        header+=["H (Oe)"]

        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,'header'))

        #######################################################
        #INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        #I_source=instr.instr_8

        voltmeter = instr.instr_2
        ppms = instr.ppms
        I_source = instr.instr_1

        #Instruments set-up

        with reserved_bus_access:
            voltmeter.switch_channel(1)
            voltmeter.setup_single_shot()
            voltmeter.set_integration_rate(f.mesure_speed)
#            voltmeter.conf_channel2()
#            voltmeter.set_integration_rate(f.mesure_speed)


#        I=f.current1
#        rate = 100
#        approach = 'Linear'
#        mode = 'Persistent'
        filterwaitime=0.0167*f.mesure_speed
        #######################################################
        #MAIN LOOP
        for I in np.arange(f.current1,f.current2,f.current3):
            #Check if the main process is telling to stop
            if self.stop_flag.isSet():
                break


            for i in range(f.repeat_points):
                if self.stop_flag.isSet():
                    break
#                Vp=0
#                Vm=0
                VpR=0
                VmR=0
                with reserved_bus_access:
                    Herror, Hexp, status = ppms.get_field()
                    #2nd order scheme to correct for the thermoelectric effect
                    #+I
#                    voltmeter.switch_channel(1)
#                    I_source.set_current_source_amplitude(I)
#                    time.sleep(filterwaitime)
#                    Vp+=voltmeter.query_voltage()/2.0
#                    #-I
#                    I_source.set_current_source_amplitude(-I)
#                    time.sleep(filterwaitime)
#                    Vm+=voltmeter.query_voltage()/2.0
#                    I_source.set_current_source_amplitude(-I)
#                    time.sleep(filterwaitime)
#                    Vm+=voltmeter.query_voltage()/2.0
#                    #+I
#                    I_source.set_current_source_amplitude(I)
#                    time.sleep(filterwaitime)
#                    Vp+=voltmeter.query_voltage()/2.0
#                    I_source.set_current_source_amplitude(0)
                    #2nd order scheme to correct for the thermoelectric effect
                    #+I
#                    voltmeter.switch_channel(2)
                    I_source.set_current_source_amplitude(I)
                    time.sleep(filterwaitime)
                    VpR+=voltmeter.query_voltage()/2.0
                    #-I
                    I_source.set_current_source_amplitude(-I)
                    time.sleep(filterwaitime)
                    VmR+=voltmeter.query_voltage()/2.0
                    I_source.set_current_source_amplitude(-I)
                    time.sleep(filterwaitime)
                    VmR+=voltmeter.query_voltage()/2.0
                    #+I
                    I_source.set_current_source_amplitude(I)
                    time.sleep(filterwaitime)
                    VpR+=voltmeter.query_voltage()/2.0
                    I_source.set_current_source_amplitude(0)

                    T = ppms.get_temperature()[1]
#                T = (T0+T1)/2.0
#                TR = (T1+T2)/2.0
#                H=(H0+H1)/2.0
#                HR=(H1+H2)/2.0
#                V = (Vp-Vm)/2.0
                VR = (VpR-VmR)/2.0

                ######Compile the latest data######
                t=time.clock()-start_time
                epochtime=time.time()
                last_data=[t,epochtime]
                last_data.append(T)
#                last_data+=[Vp,Vm,V]
                last_data+=[VpR,VmR,VR]
                last_data.append(I)
                last_data+=[Hexp]

                #print last_data
                #print map(type,last_data)
                #######Send latest data to the main process for display and storage######
                self.data_queue.put((last_data,'data'))
                #######Wait mesure_delay secs before taking next measurements
                time.sleep(f.mesure_delay)


#Multithreading
import threading
#Time measurement
import time

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
#        header+=["T Hall (K)", "T Resistivity (K)"]
        header+=["T (K)"]
        header+=["VpHall","VmHall","(VpHall-VmHall)/2"]
#        header+=["VpR","VmR","(VpR-VmR)/2"]
        header+=["I (A)"]
        header+=["H Hall (Oe)"]
#        header+=["H Hall (Oe)","H Resistivity (Oe)"]

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
            voltmeter.switch_channel(1)

        I=f.current1
        #######################################################
        #MAIN LOOP
        while True: #loop and measure indefinitely, until the main process tells to stop
            #Check if the main process is telling to stop
            if self.stop_flag.isSet():
                break


#            Vp=0
#            Vm=0
#            V=0

            VpR=0
            VmR=0
#            VR=0
            filterwaitime=0.0167*f.mesure_speed
            with reserved_bus_access:
                H0=ppms.get_field()[0]
                time.sleep(1)
                T0=ppms.get_temperature()[0]
                #2nd order scheme to correct for the thermoelectric effect
                #+I
#                voltmeter.switch_channel(1)
#                I_source.set_current_source_amplitude(I)
#                time.sleep(filterwaitime)
#                Vp+=voltmeter.query_voltage()/2.0
#                #-I
#                I_source.set_current_source_amplitude(-I)
#                time.sleep(filterwaitime)
#                Vm+=voltmeter.query_voltage()/2.0
#                I_source.set_current_source_amplitude(-I)
#                time.sleep(filterwaitime)
#                Vm+=voltmeter.query_voltage()/2.0
#                #+I
#                I_source.set_current_source_amplitude(I)
#                time.sleep(filterwaitime)
#                Vp+=voltmeter.query_voltage()/2.0
#                I_source.set_current_source_amplitude(0)
#                T1=ppms.get_temperature()[0]
#                H1=ppms.get_field()[0]
                #2nd order scheme to correct for the thermoelectric effect
                #+I
#                voltmeter.switch_channel(1)
                for i in range(f.repeat_points):
                    I_source.set_current_source_amplitude(I)
                    time.sleep(filterwaitime)
                    VpR+=voltmeter.query_voltage()/2.0/f.repeat_points
                    #-I
                    I_source.set_current_source_amplitude(-I)
                    time.sleep(filterwaitime)
                    VmR+=voltmeter.query_voltage()/2.0/f.repeat_points
                    I_source.set_current_source_amplitude(-I)
                    time.sleep(filterwaitime)
                    VmR+=voltmeter.query_voltage()/2.0/f.repeat_points
                    #+I
                    I_source.set_current_source_amplitude(I)
                    time.sleep(filterwaitime)
                    VpR+=voltmeter.query_voltage()/2.0/f.repeat_points
                    I_source.set_current_source_amplitude(0)
                T1=ppms.get_temperature()[0]

            T = (T0+T1)/2.0
#            TR = (T1+T2)/2.0
#            H=(H0+H1)/2.0
#            HR=(H1+H2)/2.0
#            V = (Vp-Vm)/2.0
            VR = (VpR-VmR)/2.0

            ######Compile the latest data######
            t=time.clock()-start_time
            epochtime=time.time()
            last_data=[t,epochtime]
            last_data.append(T)
#            last_data.append(TR)
#            last_data+=[Vp,Vm,V]
            last_data+=[VpR,VmR,VR]
            last_data.append(I)
            last_data+=[H0]

            #print last_data
            #print map(type,last_data)
            #######Send latest data to the main process for display and storage######
            self.data_queue.put((last_data,'data'))
            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)


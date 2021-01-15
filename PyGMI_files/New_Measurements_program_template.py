import threading
import time

class Script(threading.Thread):
    """
    create a separate thread to run the measurements without
    freezing the interface
    """
    def __init__(self,mainapp,frontpanel,data_queue,stop_flag,GPIB_bus_lock,
                 **kwargs):
        # nothing to modify here
        threading.Thread.__init__(self,**kwargs)
        self.mainapp = mainapp
        self.frontpanel = frontpanel
        self.data_queue = data_queue
        self.stop_flag = stop_flag
        self.GPIB_bus_lock = GPIB_bus_lock

    def run(self):
        # this is the part that will be run in a separate thread
        #######################################################
        # SHORTCUTS
        # a shortcut to the main app, especially the instruments
        m = self.mainapp
        # a shortcut to frontpanel values
        f = self.frontpanel
        # a lock that reserves the access to the GPIB bus
        reserved_bus_access = self.GPIB_bus_lock
        # a shortcut to a FIFO queue to send the data to the main thread
        #data_queue=self.data_queue
        #######################################################
        #SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        #for example if header = ["Time (s)","I (A)","V (volt)"]
        #then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"
        header = ['Time (s)']
        if f.Temp_on:header += ["T (K)"]
        if f.instr_on_1:header += ["I1"]
        if f.instr_on_2:header += ["p1","m1","V1"]
        if f.instr_on_3:header += ["I2"]
        if f.instr_on_4:header += ["p2","m2","V2"]
        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time = time.clock()
        #######################################################
        #INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        instr1 = m.instr_1
        instr2 = m.instr_2
        instr3 = m.instr_3
        instr4 = m.instr_4
        temp_controller = m.temp_controller
        #######################################################
        # SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD,
        # WHICH WILL TAKE CARE OF THE REST
        comment = 'optional comments at the top of the file'
        self.data_queue.put((comment,'comment'))
        self.data_queue.put((header,'header'))

        #######Control parameters loop(s)######
        while True:
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break
            #reserve the access to the instruments, then discuss with them
            with reserved_bus_access:
                #Measure T,H
                if f.Temp_on:
                    T = temp_controller.query_temp(f.temp_controller_channel)

                #Measure with +I
                if f.instr1_on:
                    instr1.set_current_source_amplitude(f.current1)
                    time.sleep(0.05)
                if f.instr2_on:
                    Vp1 = instr2.query_voltage()
                #Measure with -I
                if f.instr1_on:
                    instr1.set_current_source_amplitude(-f.current1)
                    time.sleep(0.05)
                if f.instr2_on:
                    Vm1 = instr2.query_voltage()
                instr1.set_current_source_amplitude(0)

                #Measure with +I
                if f.instr3_on:
                    instr3.set_current_source_amplitude(f.current2)
                    time.sleep(0.05)
                if f.instr4_on:
                    Vp2 = instr4.query_voltage()
                #Measure with -I
                if f.instr3_on:
                    instr3.set_current_source_amplitude(-f.current2)
                    time.sleep(0.05)
                if f.instr4_on:
                    Vm2 = instr4.query_voltage()
                instr3.set_current_source_amplitude(0)

            ######Compile the latest data######
            t = time.clock()-start_time
            last_data = [t]
            if f.Temp_on:last_data.append(T)
            if f.instr1_on:last_data.extend([f.current1,Vp1,Vm1,(Vp1-Vm1)/2.0])
            if f.instr3_on:last_data.extend([f.current2,Vp2,Vm2,(Vp2-Vm2)/2.0])

            #######Send the latest data to the main thread for automatic display and storage into the savefile######
            self.data_queue.put((last_data,'data'))

            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break

            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)


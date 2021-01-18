# Multithreading
import threading
# Time measurement
import time


# import numpy as np

######create a separate thread to run the measurements without freezing the front panel######
class Script(threading.Thread):
    def __init__(self, mainapp, frontpanel, data_queue, stop_flag, Instr_bus_lock, **kwargs):
        # nothing to modify here
        threading.Thread.__init__(self, **kwargs)
        self.mainapp = mainapp
        self.frontpanel = frontpanel
        self.data_queue = data_queue
        self.stop_flag = stop_flag
        self.Instr_bus_lock = Instr_bus_lock

    def run(self):
        # this is the part that will be run in a separate thread
        #######################################################
        # SHORTCUTS
        instr = self.mainapp  # a shortcut to the main app, especially the instruments
        f = self.frontpanel  # a shortcut to frontpanel values
        #        reserved_bus_access=self.Instr_bus_lock     #a lock that reserves the access to instruments
        # data_queue=self.data_queue                #a shortcut to a FIFO queue to send the data to the main thread
        #######################################################
        # SAVEFILE HEADER - add column names to this list in the same order as you will send the results of the measurements to the main thread
        # for example if header = ["Time (s)","I (A)","V (volt)"]
        # then you have to send the results of the measurements this way : "self.data_queue.put(([some time, some current, some voltage],False))"

        header = ['Time (s)', 'Time since Epoch']
        header += ["Frequency (Hz)"]
        header += ["R (Ohm)", "Theta (deg)"]
        header += ["I (A)", "V (volt)"]

        #######################################################
        # ORIGIN OF TIME FOR THE EXPERIMENT
        start_time = time.clock()
        #######################################################
        # SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header, 'header'))

        #######################################################
        # INSTRUMENTS NAMES SHORTCUTS FOR EASIER READING OF THE CODE BELOW
        hki = instr.instr_1

        #######################################################
        # MAIN LOOP
        # for f in [i * 10 ** exp for exp in range(0, 5) for i in range(1, 10)] + [100000]:
        for f in range(1, int(1e5), 50):
            # Check if the main process is telling to stop
            if self.stop_flag.isSet():
                break
            hki.set_frequency(f)
            time.sleep(2)
            V = hki.query_voltage()
            I = hki.query_current()
            R, theta = hki.query_R_theta()
            ######Compile the latest data######
            t = time.clock() - start_time
            epochtime = time.time()
            last_data = [t, epochtime, f, R, theta, I, V]

            #######Send latest data to the main process for display and storage######
            self.data_queue.put((last_data, 'data'))
            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)

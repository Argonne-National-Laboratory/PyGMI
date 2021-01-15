#Multithreading
import threading
#Time measurement
import time
#from scipy import stats

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
        header=['Time (s)','Time (min)']
        if f.instr_on_14:header+=["LHe level (%)","rate (%/min)"]
        with reserved_bus_access:
            a=m.instr14.set_unit_to_percent()
        #######################################################
        #ORIGIN OF TIME FOR THE EXPERIMENT
        start_time=time.clock()
        #######################################################
        #SEND THE HEADER OF THE SAVEFILE BACK TO THE MAIN THREAD, WHICH WILL TAKE CARE OF THE REST
        self.data_queue.put((header,'header'))
        last_t=[]
        last_L=[]
        rate=0
        def bare_bone_lin_reg(x,y):
            """give the linear coefficient only, via the analytic formula cov(X,Y)/var(X)"""
            n=len(x)
            res=(sum(x)*sum(y)-n*sum([x[i]*y[i] for i in range(n)]))/(sum(x)**2-n*sum([x[i]**2 for i in range(n)]))
            return res

        #######Control parameters loop(s)######
        while True:
            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break
            #reserve the access to the instruments, then discuss with them
            with reserved_bus_access:
                if f.instr_on_14:
                    L=float(m.instr14.query_LHe_level()[:-1])


            ######Compile the latest data######
            t=time.clock()-start_time
            last_data=[t,t/60.0]
            if f.instr_on_14:
                last_data.extend([L])
                last_L.append(L)
                last_t.append(t/60.0)
            if len(last_L)>15:
                #(rate,offset,reg_coef,reg_tt,stderr)=stats.linregress(last_t[-15:],last_L[-15:])
                rate=bare_bone_lin_reg(last_t[-15:],last_L[-15:])
            last_data.append(rate)
            #######Send the latest data to the main thread for automatic display and storage into the savefile######
            self.data_queue.put((last_data,'data'))

            #Check if the main thread has raised the "Stop Flag"
            if self.stop_flag.isSet():
                break

            #######Wait mesure_delay secs before taking next measurements
            time.sleep(f.mesure_delay)


# -*- coding: utf-8 -*-
import visa,time
from random import randrange
#print randrange(10)

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::22",*args,**kwargs):
        global current_current
        current_current=1
        self.temp=randrange(2950,2951)/10.0
        self.visa=VISA_address
        self.status='PAUSED'
        self.stat_ct=0
        #the encoding of the python script file is utf8 but the Qt interface is unicode, so conversion is needed
        self.channels_names=[]
        for txt in ['A','B','C','D']:
            self.channels_names.append(unicode(txt,encoding='utf-8'))
        print self.query_unit_Id()

    #def initialize(self,*args,**kwargs):
    def initialize(self,combobox=None):
        if combobox is not None:
            #update the combobox of the user interface with a list of all channels available for this Temp controller
            combobox.clear()
            combobox.addItems(self.channels_names)
        return 1        

    def query_unit_Id(self):
        return "Virtual instrument for test with dummy address : "+self.visa
        
    def query_dummy_measure(self,value):
        return value
    
    def query_temp(self,channel):
        return self.temp
        
    def switch_ramp(self,loop,state):
        pass
        
    def conf_ramp(self,loop,rate,state):
        pass
                        
    def set_setpoint(self,loop,T):
        self.loop=loop
        self.temp=T        
        
    def query_programmed_field(self):
        return  randrange(2950,2951)/10.0
        
    def set_current_source_amplitude(self,current):
        global current_current
        current_current=current
        #self.current=current
        
    def query_voltage(self):
        global current_current
        return current_current*randrange(111,112)/100.0+(randrange(100)-50)*1e-9
        
    def program_ramp_rate_in_Gauss_per_second(self,rate):
        self.rate=rate
    
    def program_field_in_kG(self,value):
        self.field=value
    
    def ramp_to_programmed_field(self):
        self.stat_ct=0
        self.status='RAMPING to programmed current/field'
    
    def query_status(self):
        self.stat_ct+=1
        if self.stat_ct>5:
            self.status='HOLDING at the programmed current/field'
        return self.status


# -*- coding: utf-8 -*-
import visa

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::12"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print self.query_unit_Id()
        #the encoding of the python script file is utf8 but the Qt interface is unicode, so conversion is needed
        self.channels_names=[]
        for txt in ['A','B','C','D']:
            self.channels_names.append(unicode(txt,encoding='utf-8'))

    def initialize(self,combobox=None):
        if combobox is not None:
            #update the combobox of the user interface with a list of all channels available for this Temp controller
            combobox.clear()
            combobox.addItems(self.channels_names)
        

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def query_temp(self,channel):
        #reports the current temperature reading on any of the input channels
        #channel can be A,B,C,D
        return float(self.io.query("KRDG? "+channel))
    
    def query_Status_Byte(self):
        return bin(int(self.io.query("*STB?")))[2:]
    
    def query_status_enabled_byte(self):
        """Ramp Done,SRQ,ESB,Error,Alarm,Settle,New OPT,New A&B"""
        return bin(int(self.io.query("*SRE?")))[2:]
        
    def enable_status_byte_service_request(self,b):
        """If the Service Request is enabled, any of these bits being set causes the Model 340 to pull the SRQ management low to signal the BUS CONTROLLER"""
        self.io.write("*SRE "+str(int(b,2)))
        
    def set_local_mode(self):
        self.io.write("MODE 1")
    
    def set_remote_mode(self):
        self.io.write("MODE 2")
        
    def conf_ramp(self,loop=1,rate=None,on_off='on'):
        """
        Configures the control loop ramp.
        <loop> Specifies which loop to configure.
        <off/on> Specifies whether ramping is off or on.
        <rate K/min> Specifies how many kelvin per minute to ramp to the setpoint.
        When Control <loop> setpoint is changed, ramp the current setpoint to the target setpoint at <rate K/minute>.
        """
        conv={'on':'1','off':'0'}
        self.io.write("RAMP "+str(loop)+', '+conv[on_off]+', '+str(rate))
    
    def switch_ramp(self,loop,on_off='on'):
        conv={'on':'1','off':'0'}
        self.io.write("RAMP "+str(loop)+', '+conv[on_off])
        
        
    def set_heater_range(self,value):
        """Valid entries: 0 - 5."""
        self.io.write("RANGE "+str(value))
#50 Ohm, 1A:
        #{'off':0,'5mW':1,'50mW':2,'500mW':3,'5W':4,'50W':5}

               
    def set_setpoint(self,loop=1,temperature=2):
        """Configures the control loop setpoint.
        <loop> Specifies which loop to configure.
        <temperature> The value for the setpoint (in whatever units the setpoint is using)."""
        self.io.write("SETP "+str(loop)+', '+str(temperature))   
    
    def query_PID(self,loop):
        return map(float,self.io.query('PID? '+str(loop)).split(','))
        
    def set_PID(self,loop,P,I,D):
        self.io.write('PID '+str(loop)+','+str(P)+','+str(I)+','+str(D))
    
    def query_setpoint(self,loop=1):
        return self.io.query("SETP? "+str(loop))
    

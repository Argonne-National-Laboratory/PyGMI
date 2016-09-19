# -*- coding: utf-8 -*-
import visa
import time

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::17"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print self.io.query("*IDN?")
        sens_list_utf8=['10 mV','100 mV','1 V','10 V','100 V']
        self.sens_list_num=[0.01,0.1,1,10,100]
        #the encoding of the python script file is utf8 but the Qt interface is unicode, so conversion is needed
        self.sensitivity=[]
        for txt in sens_list_utf8:
            self.sensitivity.append(unicode(txt,encoding='utf-8'))

    def initialize(self):
        """commands executed when the instrument is initialized"""
        self.reset_and_query_voltage()
        self.io.write(':SYSTem:LSYNc:STATe ON')
        self.set_integration_rate(3)
        #self.setup_single_shot_Tlink()

    def reset_autozero(self,duration=1):
        self.io.write(':SYSTem:AZERo:STATe ON')
        self.io.write(':syst:faz ON')
        time.sleep(duration)
        self.io.write(':syst:faz off')
        self.io.write(':SYSTem:AZERo:STATe OFF')

    def conf_channel2(self):
        lnanoV=[':SENS:CHAN 2',':CONF:VOLT',':INIT:CONT OFF']
        for txt in lnanoV:
            self.io.write(txt)

    def switch_channel(self,chan=1):
        self.io.write(':SENS:CHAN '+str(chan))

    def setup_single_shot(self,verbose=False):
        print "configuring Keithley2182A for continuously taking low speed single shot readings"
        lnanoV=[':syst:pres', # 2182 - System preset defaults.
                ':CONF:VOLT',
                ':INIT:CONT OFF']
        for txt in lnanoV:
            if verbose:
                print txt
            self.io.write(txt)

    def setup_single_shot_Tlink(self,verbose=False):
        print "configuring Keithley2182A for a single shot with trigger link cable"
        lnanoV=[':syst:pres', # 2182 - System preset defaults.
                ':CONF:VOLT',
                ':SENSe:VOLTage:DC:RANGe 0.0001',
                ':SENSe:VOLTage:DC:LPASs OFF',
                ':SENSe:VOLTage:DC:DFILter OFF',
                ':TRIG:DEL:AUTO OFF',
                ':trig:del 0',
                ':SENS:VOLT:NPLC 0.1',
                ':DISPlay:ENABle ON',
                #':sens:volt:delta on',
                ':syst:faz off',
                ':SYSTem:AZERo:STATe OFF',
                ':trig:sour ext',
                #':trac:poin '+buff_pts,
                ':SYSTem:LSYNc:STATe ON',
                #':trac:feed:cont next',
                ':trig:coun inf',
                ':SAMP:COUN 1',
                ':INIT']

        for txt in lnanoV:
            if verbose:
                print txt
            self.io.write(txt)
        time.sleep(1) #init needs at least one second to complete
        
    def setup_sensitivity_combobox(self,comboBox):
        comboBox.clear()        
        comboBox.addItems(self.sensitivity)                

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def reset_and_query_voltage(self):
        """This query is much slower than a “:READ?” or “:FETCh?” query because it has to
reconfigure the instrument each time it is sent. It will reset the NPLC, autoranging, and
averaging to default settings."""
        return float(self.io.query(":MEAS:VOLT?"))

##:READ? :This command performs three actions. It will reset the trigger model to the idle layer
##(equivalent to the :ABORt command), take the trigger model out of idle (equivalent to the :INIT
##command), and return a reading (equivalent to a “FETCh?” query). This command will always
##return a new reading, since aborting the trigger model will invalidate any old readings and
##trigger a new one. This query will “wait” for a new reading to become available before the
##instrument sends a result back.
##    This command won’t work if the trigger source is set for BUS or EXTERNAL. This will
##cause a –214, “Trigger deadlock” error. Under this condition, one should use a “:FETCh?” query
##or a “:DATA:FRESh?” query (see page H-4). If the trigger model is continuously initiating
##(:INIT:CONT ON), sending this query may cause a –213, “Init ignored” error, but will still give
##a new reading.
    def query_voltage(self):
        return float(self.io.query(":READ?"))
    
    def query_latest_reading(self):
        """This command does not trigger a measurement. The command simply requests the last
available reading. Note that this command can repeatedly return the same reading."""
        return float(self.io.query(':FETCh?'))

    def query_latest_fresh_reading(self):
        """This query is similar to the “:FETCh?” in that it returns the latest reading from the instrument,
but has the advantage of making sure that it does not return the same reading twice."""
        return float(self.io.query(':sens:data:fresh?'))

#:MEASure:<function>?
#Parameters
#<function> = VOLTage[:DC] Voltage
#TEMPerature Temperature
#Description
#This command combines all of the other signal oriented measurement commands to perform
#a “one-shot” measurement and acquire the reading.
#When this command is sent, the following commands execute in the order that they are
#presented.
#:ABORt
#:CONFigure:<function>
#:READ?
#When :ABORt is executed, the instrument goes into the idle state if continuous initiation is
#disabled. If continuous initiation is enabled, the operation re-starts at the beginning of the
#Trigger Model.
#When :CONFigure is executed, the instrument goes into a “one-shot” measurement mode.
#See :CONFigure for more details.
#When :READ? is executed, its operations will then be performed. In general, another
#:ABORt is performed, then an :INITiate, and finally a :FETCh? to acquire the reading. See
#“:READ?” for more details.

    def select_channel(self,chan):
        self.io.write(':SENS:CHAN '+str(chan))

#Select channel to measure; 0, 1 or 2 (0 = internal temperature sensor).

    def output_terminals(self,side):
        if side=='rear':
            self.io.write(':ROUT:TERM REAR')
        elif side=='front':
            self.io.write(':ROUT:TERM FRON')
    
#:ROUTe:TERMinals <name> Select front or rear panel in/out jacks
#Parameters <name> = FRONt Front panel in/out jacks
#REAR Rear panel in/out jacks
#Query :TERMinals? Query state of front/rear switch setting

    def output_ON(self):
        self.io.write(':OUTP 1')
    
    def output_OFF(self):
        self.io.write(':OUTP 0')
        
#Enable or disable analog output (OFF forces 0V).

    def current_source_range(self,RANGe):
        self.io.write(':SOUR:CURR:RANG '+str(RANGe))

    def voltage_source_range(self,RANGe):
        self.io.write(':SOUR:CURR:RANG '+str(RANGe))

    def set_integration_rate(self,NPLC):
        self.io.write(':SENS:VOLT:NPLC '+str(NPLC))

    def set_sensitivity(self,RANGE):
        self.io.write(':SENS:VOLT:RANG '+str(RANGE))

# -*- coding: utf-8 -*-
import visa

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB::12"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print(self.io.query("*IDN?"))
        #the encoding of the python script file is utf8 but the Qt interface
        # is unicode, so conversion is needed
        self.channels_names=[]
        for txt in ['A','B']:
            self.channels_names.append(str(txt))

    def initialize(self,combobox=None):
        if combobox is not None:
            #update the combobox of the user interface with a list of all channels available for this Temp controller
            combobox.clear()
            combobox.addItems(self.channels_names)

    def query_temp(self,channel):
        #reports the current temperature reading on any of the input channels
        #channel can be 0,1/CHA,CHB/A,B
        return float(self.io.query("INP? "+channel))

    def query_resistance(self,channel):
        return float(self.io.query('INP '+channel+':SENPR?'))

    def query_temp_unit(self,channel):
        #the display units indicator will be K, C, F, V for Volts or O for Ohms
        if channel in ['0','1','CHA','CHB','A','B']:
            return self.io.query("INP "+channel+":UNIT?")
        else:
            raise ValueError

    def set_unit(self,channel,unit):
        if unit in ['K', 'C', 'F', 'V', 'O'] and channel in ['0','1','CHA','CHB','A','B']:
            self.io.write('INP '+channel+':UNIT '+unit)
        else:
            raise ValueError

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def clear_status(self):
        self.io.write('*cls')

    def reset(self):
        self.io.write('*RST')

    def disengage(self):
        #disengage control loops
        self.io.write('*STOP')

    def engage(self):
        #engage control loops that are enabled
        self.io.write('CONT')

    def is_engaged(self):
        #query status of the loops
        return self.io.query('CONT?')
        #the command 'SYST:LOOP?' seems to do exactly the same

    def set_remote_mode(self):
        #lock out the front panel keypad
        self.io.write('SYST:LOCK ON')

    def set_local_mode(self):
        #unlock the front panel keypad
        self.io.write('SYST:LOCK OFF')

    def is_locked(self):
        #query the status of the lock of the front panel keypad
        return self.io.query('SYST:LOCK?')

    def save_config(self):
        #This saves the entire instrument configuration to flash
        #memory so that it will be restored on the next power-up.
        self.io.write('SYST:NVS')

    def beep(self,duration):
        self.io.write('SYST:BEEP '+str(int(duration)))

    def query_disp_TC(self):
        return self.io.query('SYST:DIST?')

    def set_disp_TC(self,tc):
        #<tc> is the display filter time constant, in seconds, selected from the
        #following list: 0.5, 1, 2, 4, 8, 16, 32, 64.
        self.io.write('SYST:DIST'+str(tc))

    def reseed(self):
        self.io.write('SYS:RES')

    def query_internal_temperature(self):
        #The Model 32 incorporates a temperature sensor into it's internal voltage
        #reference. This temperature is essentially the internal temperature of the instrument
        return self.io.query('SYST:AMB?')




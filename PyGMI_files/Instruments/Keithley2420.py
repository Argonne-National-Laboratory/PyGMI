# -*- coding: utf-8 -*-
import visa
import time

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::17"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print(self.io.query("*IDN?"))

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def initialize(self):
        """commands executed when the instrument is initialized"""
        #self.source_mode('I')
        #self.enable_current_autorange(True)
        #self.set_current_source_amplitude(0.0)
        #self.current_source_range_auto()
        #self.set_voltage_compliance(20)
        #self.output_ON()
        pass

    def setup_single_shot_Tlink(self,verbose=False):
        print("configuring Keithley2400 series for pulsed mode")
        self.output_OFF()
        #self.current_source_range(0.03)
        self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*rst',
                   'source1:clear:auto ON', # SM - turn on auto output-off
                   ':arm:dir sour', # SM - diable bypass of the arm layer event detector
                   #':arm:sour bus', # SM - enable to trigger the arm layer from the bus
                   ':arm:outp none', # SM - disable the arm layer output trigger
                   ':trig:dir sour', # SM - Enable source event detector bypass
                   ':trig:inp del', # SM - enable the Delay Event Detector
                   ':trig:sour tlin', # SM - Select T-link cable as trigger source
                   ':trig:ilin 1', # SM - receive triggers on line 1 of the T-link
                   ':trig:olin 2', # SM - send triggers on line 2 of the T-link
                   ':trig:outp sour', # SM - Output trigger after source has reached the set level
                   ':trig:coun 1', # SM - single shot
                   ':trig:del 0',
                   ':sens:func:off:all', # SM - Disable all measurement functions
                   #':sens:func volt',
                   #':volt:nplc 0.01', # SM - Fast measurements
                   ':sour:curr:mode fix'] # SM - Enable fixed mode.
                   #':sour:curr 1e-3'] # SM - Immediately update the amplitude of a fixed source
                   #':outp on', # SM - Turn output on.
                   #':init'] # SM - Start sweep.

        for txt in ldcSource:
            if verbose:
                print(txt)
            self.io.write(txt)
        time.sleep(1)
        self.source_mode('I') # SM - Select source current mode

    def setup_single_shot(self,verbose=False):
        print("configuring Keithley2400 series for continuous mode")
        self.output_OFF()
        self.io.write(':SYST:BEEP:STAT 0')
        ldcSource=['*rst',
                   ':SOUR:FUNC CURR',
                   ':sour:clear:auto ON', # SM - turn on auto output-off
                   ':SOUR:CURR:RANG:AUTO 1', # SM - enable auto-range
                   ':sour:curr:mode fix', # SM - Enable fixed mode.
                   ':sour:curr 0', # SM - Immediately update the amplitude of a fixed source
                   ':outp on'] # SM - Turn output on.


        for txt in ldcSource:
            if verbose:
                print(txt)
            self.io.write(txt)

    def setup_single_shot2(self):
        self.io.write('*rst')
        self.io.write(':SOUR:FUNC CURR')
        self.io.write('sour:clear:auto ON')
        self.io.write(':SOUR:CURR:RANG:AUTO 1')
        self.io.write(':sour:curr:mode fix')
        self.io.write(':sour:curr 0')
        self.io.write(':outp on')

    def output_ON(self):
        self.io.write(':OUTP 1')

    def output_OFF(self):
        self.io.write(':OUTP 0')

    def output_terminals(self,side):
        if side=='rear':
            self.io.write(':ROUT:TERM REAR')
        elif side=='front':
            self.io.write(':ROUT:TERM FRON')


    def source_mode(self,mode):
        if mode=='V':
            self.io.write(':SOUR:FUNC VOLT')
        elif mode=='I':
            self.io.write(':SOUR:FUNC CURR')
        elif mode=='memory':
            self.io.write(':SOUR:FUNC MEM')

    def current_source_range(self,RANGe):
        self.io.write(':SOUR:CURR:RANG '+str(RANGe))

    def voltage_source_range(self,RANGe):
        self.io.write(':SOUR:VOLT:RANG '+str(RANGe))

    def voltage_source_autorange(self):
        self.io.write(':SOUR:VOLT:RANG:AUTO 1')

    def current_source_autorange(self):
        self.io.write(':SOUR:CURR:RANG:AUTO 1')



    def set_current_source_amplitude(self,amp):
        self.io.write(':SOUR:CURR '+str(amp))

    def set_voltage_source_amplitude(self,amp):
        self.io.write(':SOUR:VOLT '+str(amp))

    def set_voltage_compliance(self,voltage):
        self.io.write(':SENS:VOLT:PROT '+str(voltage))

    def set_current_compliance(self,amp):
        self.io.write(':SENS:CURR:PROT '+str(amp))


    def start_cycle(self):
        self.io.write(':init')

    def set_input_trigger_port(self,nb):
        self.io.write(':trig:ilin '+str(nb))    # SM - receive triggers on line 1 of the T-link

    def set_output_trigger_port(self,nb):
        self.io.write(':trig:olin '+str(nb))    # SM - send triggers on line 2 of the T-link


    def setup_voltage_measurements(self):
        self.io.write('*rst')
        self.io.write(':SOUR:FUNC CURR')
        self.io.write('sour:clear:auto ON')#enable auto output-off
        self.io.write(':SOUR:CURR:RANG:AUTO 1')
        self.io.write(':sour:curr:mode fix')
        self.io.write(':sour:curr 0')
        self.io.write(":conf:volt") #set sensing to volt, and prepare the trigger model for single shot acquisition
        self.io.write(":SYSTem:RSEN 1") #to allow 4 wire measurements (it's 2 wires by default)
        self.io.write(":format:elements volt") #to configure what data elements are returned, by default it's  (VOLTage, CURRent,RESistance, TIME, and STATus). We just want volt.

    def set_integration_rate(self,NPLC):
        self.io.write(':SENS:VOLT:NPLC '+str(NPLC))

    def query_voltage(self):
        return float(self.io.query(":READ?"))

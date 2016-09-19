# -*- coding: utf-8 -*-
import visa

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::22"):
        #part to be run at instrument initialization, the following commands are mandatory
        self.io = visa.ResourceManager().open_resource(VISA_address)
        self.VISA_address=VISA_address
        print self.query_unit_Id()

    #mandatory function
    #return instrument identification. This command is common to almost all GPIB instruments. Modify if necessary.
    def query_unit_Id(self):
        return self.io.query("*IDN?") 

    #mandatory function that will be called just after the computer successfully connected to the instrument.
    #If you don't need it, just leave it empty but do leave the command "return 1"
    def initialize(self):
        ####your initialization commands
        self.io.write("set:type:voltmeter") #dummy example in pseudo SCPI language
        print "setting the instrument to voltmeter" #dummy information to the user
        ####
        return 1        

    #define the functions that you want accessible in your measurements program for that type of instrument

    #DUMMY examples of functions. Check the manual of your instrument to find the right commands for you

    #The command self.io.ask sends ":READ?" to the instrument, then wait for the answer, and return the string sent back by the instrument. #Since we expect this string to contain a voltage, the string is converted to float.
    #The function finally return this float value
    def query_voltage(self): 
        return float(self.io.query(":READ?")) 
            
    #This function has to be called with some user-provided value "amp"
    #we convert that value to a string "str(amp)"
    #then we send the SCPI command ':SOUR:CURR '+str(amp) to the instrument. We don't wait for an answer.
    def set_current_source_amplitude(self,amp):
        self.io.write(':SOUR:CURR '+str(amp))

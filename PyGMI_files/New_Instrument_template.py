# -*- coding: utf-8 -*-
import visa

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::22"):
        """
        part to be run at instrument initialization,
        the following commands are mandatory
        """
        self.io = visa.ResourceManager().open_resource(VISA_address)
        self.VISA_address = VISA_address
        print(self.query_unit_Id())

    def query_unit_Id(self):
        """
        mandatory function
        return instrument identification.
        This command is common to almost all GPIB instruments.
        Modify if necessary.
        """
        return self.io.query("*IDN?")

    def initialize(self):
        """
        mandatory function that will be called just after the computer
        successfully connected to the instrument.
        If you don't need it, just leave it empty but do leave the command
        "return 1"
        """
        # your initialization commands
        # dummy example in pseudo SCPI language
        self.io.write("set:type:voltmeter")
        # dummy information to the log
        print("setting the instrument to voltmeter")
        return 1

    # below, define the functions that you want accessible in your
    # measurements program for that type of instrument

    # Those are DUMMY examples
    # Check the manual of your instruments to find the right commands

    def query_voltage(self):
        """
        The command self.io.ask sends ":READ?" to the instrument,
        then wait for the answer, and return the string sent back by the
        instrument. #Since we expect this string to contain a voltage,
        the string is converted to float.
        The function finally return this float value
        """
        return float(self.io.query(":READ?"))

    def set_current_source_amplitude(self,amp):
        """
        This function has to be called with some user-provided value "amp"
        we convert that value to a string "str(amp)"
        then we send the SCPI command ':SOUR:CURR '+str(amp) to the instrument.
        We don't wait for an answer.
        """
        self.io.write(':SOUR:CURR '+str(amp))

# -*- coding: utf-8 -*-
import visa

class Connect_Instrument():
    def __init__(self,VISA_address="ASRL5::INSTR"):
        self.io = visa.ResourceManager().open_resource(VISA_address)

    def initialize(self):
        return 1

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def set_frequency(self,f):
        """set the reference frequency"""
        self.io.write(":FREQ"+str(f))

    def query_frequency(self):
        """query the reference frequency"""
        return float(self.io.query(":FREQ?"))

    def query_voltage(self):
        return float(self.io.query(":LEV:VOLT?"))

    def query_current(self):
        return float(self.io.query(":LEV:CCURR?"))

    def query_R_theta(self):
        return float(self.io.query(":MEAS?"))

    def query_phase(self):
        return float(self.io.query('PHAS?'))
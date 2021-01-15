# -*- coding: utf-8 -*-

import serial
#import time
class Connect_Instrument():
    def __init__(self,COM_port="COM3"):
        #Serial(N) open COM port N+1, e.g. "2" for "COM3"
        self.io = serial.Serial(float(COM_port.strip("COM"))-1,baudrate=9600, bytesize=8, parity='N', stopbits=1)
        self.io.write('F,C')
        #"F" puts the VXM On-Line
        #"C" clear the previous Index command from the VXM's memory
        #
        self.last_known_angle=290
        self.COM_port=COM_port
        #print self.query_unit_Id()

    def query_unit_Id(self):
        return "VXM step motor on port :"+self.COM_port

    def initialize(self):
        """commands executed when the instrument is initialized"""
        pass

    def relative_move(self,angle,angular_speed=1):
        """angle in degrees (+ = CCW, - = CW), angular_speed in degrees per second"""
        #minus sign is necessary so that
        #angle>0 corresponds to a trigonometrical/CCW rotation and
        #angle<0 corresponds to antitrigo/ClockWise
        #timeout in milliseconds for PyVisa > 1.5
        self.io.timeout=1000*(10+abs(angle/float(angular_speed)))
        motor_steps=-int(angle/0.015)
        motor_speed=int(angular_speed/0.015)
        self.io.write('C,S1M'+str(motor_speed)+',I1M'+str(motor_steps)+',R')
        self.io.inWaiting()
        ans=self.io.read(1)
        if ans == '^':
            self.last_known_angle+=angle
            print("rotation completed, current position:",self.last_known_angle,"degrees")


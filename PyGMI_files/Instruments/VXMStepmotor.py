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
        self.io.timeout=10+abs(angle/angular_speed)
        motor_steps=-int(angle/0.015) 
        motor_speed=int(angular_speed/0.015)
        self.io.write('C,S1M'+str(motor_speed)+',I1M'+str(motor_steps)+',R')
        self.io.inWaiting()
        ans=self.io.read(1)
        if ans == '^':
            self.last_known_angle+=angle
            print "rotation completed, current position:",self.last_known_angle,"degrees"
##a=VXM()     
##time.sleep(10)
##for i in range(10):
##    a.io.write('C,I1M-200,R')
##    time.sleep(5)

#the gear ratio is 60:1
#the step motor has 200 steps per revolution
#But the VXM also uses step units for Index and Speed parameters. One step is 1/400 of a motor
#revolution.
#so 400 steps correspond to 360/60=6 degrees
#so 6/400 = 0.015 degrees/step
#so 400/6 = 66.67 step/degrees
##        
##    def query_temp(self,channel):
##        #reports the current temperature reading on any of the input channels
##        #channel can be A,B,C,D
##        return float(self.io.ask("KRDG? "+channel))
##

##To put the VXM in the On-Line mode/programming mode, the host must send either an
##" ", or " ". When the Controller receives an " ", or " " the On-line light will light and the
##Jog inputs will be disabled.
##The " " puts the VXM on-line with echo "on" (echoes all characters received back to the
##host). The " " puts the VXM on-line with echo "off".

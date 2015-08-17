# -*- coding: utf-8 -*-
import serial
import time

class Connect_Instrument():
    def __init__(self,COM_port="COM1"):
        #Serial(N) open COM port N+1, e.g. "2" for "COM3"
        self.io = serial.Serial(float(COM_port.strip("COM"))-1,baudrate=9600, bytesize=8, parity='N', stopbits=1)
        print self.query_unit_Id()

    def read_one_answer(self):
        chars_toread=True
        ans=''
        calls=0
        while chars_toread:
            ans_len=self.io.inWaiting()
            ans+=self.io.read(ans_len)
            if '\r\n' in ans:
                chars_toread=False
            else:
                time.sleep(0.01)
            calls+=1
        #print '# calls:',calls
        return ans

        
    def query_unit_Id(self):
        """return unit firmware version"""
        self.io.write('V')
        ans=self.read_one_answer()
        if 'Firmware Version' in ans:
            return ans
        else:
            return 'Instrument did not answer to identification request'

    def initialize(self):
        """commands executed when the instrument is initialized"""
        pass
    
    def query_position(self):
        """return switch position : A,B,C,D"""
        self.io.write('S')
        ans=self.read_one_answer()
        #print ans
        if ans[-3] in 'ABCD':
            return ans[-3]
        else:
            return '0'

    def switch_to_position(self,pos):
        """switch to position : A,B,C,D"""
        if pos in 'ABCD':
            self.io.write(pos)
            time.sleep(0.04)
            ans=self.read_one_answer()
            #print 'switching to', ans
            time.sleep(0.3)
            #while self.query_position()!=pos:
            #    time.sleep(0.1)
            return 1
        else:
            print 'unrecognized channel name'
            return 0

    def scan_channels(self,repetition):
        t0=time.clock()
        for i in range(repetition):
            for j in 'ABCD':
                t1=time.clock()
                self.switch_to_position(j)
                #time.sleep(0.05)
                #while self.query_position()!=j:
                #    time.sleep(0.1)
                t2=time.clock()
                print t2-t1
                
#Serial Communication Configuration
#Baud rate = 9600, Data bits=8,Parity=None,Stop bits=1,Flow control=None
########################
#Remote Control Commands
#All commands are ASCII commands. Do not press the Enter key at the end of a command. All responses are terminated with a carriage return (‘\r’) followed by a new line feed (‘\n’).
#Command        Function                        Response
#A, a           Switch to the A position        100 Position: A
#B, b           Switch to the B position        101 Position: B
#C, c           Switch to the C position        102 Position: C
#D, d           Switch to the D position        103 Position: D
#S, s           Query position/status           10X Position: <A/B/C/D>
#V, v           Query firmware version number   901 M7215, Firmware Version 1.1, Compiled <Date>

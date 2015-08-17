# -*- coding: utf-8 -*-
import visa,time

# Retry decorator with return
def retry_with(tries=2,ans_type=int,default_ans=-1,wait=15):
    '''Retries a function or method until it returns an answer of the right type
    (e.g. int,float,str) and does not raise not an exception. If it runs out of tries
    a default answer is returned.
    '''
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries = tries # make mutable
            success=False
            while mtries >0 and not(success):
                try:
                    ans = f(*args, **kwargs) # first attempt
                    success=(type(ans)==ans_type)
                except:
                    print 'I/O COM error'
                    success=False
                    mtries -= 1      # consume an attempt
                    try:
                        f.im_self.io.read() #read and empty the buffer in case a message got stuck
                        print 'I/O buffer was reset'
                    except:
                        print 'I/O buffer could not be reset'
                    time.sleep(wait)
            if success:
                res=ans
            else:
                print "ran out of retries: exception with function", f.func_name
                res=default_ans # Ran out of tries :-(
            return res
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator

# Retry decorator without return
def retry(tries=2,wait=1):
    '''Retries a function or method until it does not raise not an exception.
    If it runs out of tries, nothing is done, and the program continue.
    '''
    def deco_retry(f):
        def f_retry(*args, **kwargs):
            mtries = tries # make mutable
            success=False
            while mtries >0 and not(success):
                try:
                    f(*args, **kwargs) # first attempt
                    success=True
                except:
                    print 'I/O COM error'
                    success=False
                    mtries -= 1      # consume an attempt
                    try:
                        f.im_self.io.read() #read and empty the buffer in case a message got stuck
                        print 'I/O buffer was reset'
                    except:
                        print 'I/O buffer could not be reset'
                    time.sleep(wait)
            if not(success):
                print "ran out of retries: exception with function", f.func_name
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::22"):
        self.io = visa.instrument(VISA_address)
        print self.query_unit_Id()
        self.last_known_field_value_in_T=0.0
        print "last known persistent field value in magnet",self.last_known_field_value_in_T,"T"
       
    def initialize(self):
        return 1    

    def query_unit_Id(self):
        return self.io.ask("*IDN?")
    
#PPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPPP
    def pause(self):
        self.io.write('pause')

    @retry(tries=5,wait=15)
    def persistent_switch_heater_ON(self,block=True):
        """if block=True, block until the persistent switch has finished heating"""
        self.io.write('PS 1')
        if block:
            stat=self.query_status()
            while stat=='Heating persistent switch' or stat=='COM error':
                time.sleep(15)
                stat=self.query_status()
                

    @retry(tries=5,wait=15)        
    def persistent_switch_heater_OFF(self):
        self.io.write('PS 0')

    @retry_with(tries=5,ans_type=str,default_ans='9999 T',wait=15)
    def program_field_in_tesla(self,field):
        if abs(field)<=9.0: #9T magnet
            self.io.write('conf:field:units 1')
            self.io.write('CONF:FIELD:PROG '+str(field))
            if self.query_persistent_switch_state()=='ON':
                self.last_known_field_value_in_T=field
        return str(self.query_programmed_field())+' '+self.query_field_unit()

    @retry_with(tries=5,ans_type=str,default_ans='99990000 G',wait=15)    
    def program_field_in_kG(self,field):
        if abs(field)<=90: #9T magnet
            self.io.write('conf:field:units 0')
            self.io.write('CONF:FIELD:PROG '+str(field))
            if self.query_persistent_switch_state()=='ON':
                self.last_known_field_value_in_T=field/10.0
        return str(self.query_programmed_field())+' '+self.query_field_unit()

    @retry_with(tries=5,ans_type=str,default_ans='9999 Tesla/second',wait=15)
    def program_ramp_rate_in_T_per_second(self,rate,bypass=False):
        if abs(rate)<=0.0200 or bypass: #9T magnet limit
            self.io.write('conf:field:units 1')
            self.io.write('conf:RAMP:RATE:UNITS 0')
            self.io.write('conf:ramp:rate:field '+str(rate))
        return str(self.query_ramp_rate())+' '+self.query_ramp_rate_unit()
    
    @retry_with(tries=5,ans_type=str,default_ans='99990000 Gauss/second',wait=15)
    def program_ramp_rate_in_Gauss_per_second(self,rate):
        if abs(rate)<=200: #9T magnet limit
            self.io.write('conf:field:units 0')
            self.io.write('conf:RAMP:RATE:UNITS 0')
            self.io.write('conf:ramp:rate:field '+str(rate*1e-3))
        return str(self.query_ramp_rate())+' '+self.query_ramp_rate_unit()

#QQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQQ
    @retry_with(tries=5,ans_type=str,default_ans='COM error',wait=15)
    def query_field_unit(self):
        conversion={'0':'kilogauss','1':'Tesla'}
        return conversion[self.io.ask('field:units?')]
    
    @retry_with(tries=5,ans_type=str,default_ans='COM error',wait=15)
    def query_persistent_switch_state(self):
        conversion={'0':'OFF','1':'ON'}
        return conversion[self.io.ask('ps?')]
    
    @retry_with(tries=5,ans_type=float,default_ans=-1.0,wait=15)
    def query_programmed_field(self):
        return float(self.io.ask('field:prog?'))
    
    @retry_with(tries=5,ans_type=float,default_ans=-1.0,wait=15)
    def query_ramp_rate(self):
        return float(self.io.ask('RAMP:RATE:FIELD?'))

    @retry_with(tries=5,ans_type=str,default_ans='COM error',wait=15)        
    def query_ramp_rate_unit(self):
        conversion={'0':'second','1':'minute'}
        return self.query_field_unit()+'/'+conversion[self.io.ask('RAMP:RATE:UNITS?')]

    @retry_with(tries=5,ans_type=str,default_ans='COM error',wait=15)
    def query_status(self):
        conversion=['RAMPING to programmed current/field',
                    'HOLDING at the programmed current/field',
                    'PAUSED',
                    'Ramping in MANUAL UP mode',
                    'Ramping in MANUAL DOWN mode',
                    'ZEROING CURRENT (in progress)',
                    'Quench detected',
                    'Heating persistent switch',
                    'AT ZERO current']
        return conversion[int(self.io.ask("STATE?"))-1]
    
#RRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR
    @retry(tries=5,wait=15)
    def ramp_to_programmed_field(self):
        self.io.write('RAMP')
        
    @retry(tries=5,wait=15)
    def wait_for_field_to_ramp(self,check_period=2):
        test=True
        while test:
            stat=self.query_status()        
            test=(stat=='RAMPING to programmed current/field' or stat=='COM error')
            #I use 0.5 for check period, and timeout error appears sometimes->now protected through "try" in query_status
            time.sleep(check_period)
                
#SSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS
    def set_field_unit_to_Tesla(self):
        self.io.write('conf:field:units 1')
        return self.query_field_unit()

    def set_field_unit_to_kGauss(self):
        self.io.write('conf:field:units 0')
        return self.query_field_unit()

    @retry(tries=5,wait=15)
    def set_magnet_to_zero(self):
        if self.query_status()=='PAUSED' or self.query_status()=='HOLDING at the programmed current/field':
            self.set_field_unit_to_Tesla()
            if self.query_persistent_switch_state()=='OFF':
                if self.last_known_field_value_in_T!=self.query_programmed_field():
                    self.program_field_in_tesla(self.last_known_field_value_in_T)
                    self.ramp_to_programmed_field()
                    self.wait_for_field_to_ramp()                 
                self.persistent_switch_heater_ON(block=True)
            self.program_ramp_rate_in_T_per_second(0.0200)
            self.program_field_in_tesla(0)
            self.ramp_to_programmed_field()
            print "ramping magnet to zero"
            self.wait_for_field_to_ramp()

    #@retry(tries=2,wait=10)
    def set_field_in_Tesla(self,field):
        if self.query_status()=='PAUSED' or self.query_status()=='HOLDING at the programmed current/field':
            self.set_field_unit_to_Tesla()
            if self.query_persistent_switch_state()=='OFF':
                while self.last_known_field_value_in_T!=self.query_programmed_field():
                    self.program_ramp_rate_in_T_per_second(0.0200,bypass=True)
                    self.program_field_in_tesla(self.last_known_field_value_in_T)
                    self.ramp_to_programmed_field()
                    print "matching power supply to last known field value",self.last_known_field_value_in_T,"T"
                    self.wait_for_field_to_ramp()
                while self.program_ramp_rate_in_T_per_second(0.02)!='0.02 Tesla/second':
                    pass
                print "heating persistent switch, then waiting 1 min"
                self.persistent_switch_heater_ON(block=True)
                time.sleep(60)
            while self.program_ramp_rate_in_T_per_second(0.02)!='0.02 Tesla/second':
                pass                
            self.program_field_in_tesla(field)
            self.ramp_to_programmed_field()
            print "ramping magnet to",field,"T, then waiting 1 min"
            self.wait_for_field_to_ramp()
            time.sleep(60)
            
            self.persistent_switch_heater_OFF()
            print "waiting 2 min for persistent switch to cool down"
            time.sleep(120)
            print "ramping the power supply back to zero"
            self.program_ramp_rate_in_T_per_second(0.02,bypass=True)
            self.program_field_in_tesla(0)
            self.ramp_to_programmed_field()
            self.wait_for_field_to_ramp()
            while self.program_ramp_rate_in_T_per_second(0.02)!='0.02 Tesla/second':
                pass
        

    def set_ramp_unit_to_second(self):
        self.io.write('conf:RAMP:RATE:UNITS 0')
        return self.query_ramp_rate_unit()

    def set_ramp_unit_to_minute(self):
        self.io.write('conf:RAMP:RATE:UNITS 1')
        return self.query_ramp_rate_unit()

    
##3.4.1 Procedure for Entering Persistent Mode
##In order to enter the persistent mode of magnet operation, the operator
##should perform the following steps:
##1. Use either the programmed or manual ramping modes of the Model
##420 to achieve the desired current or field.
##2. The Model 420 should be in either the HOLDING or PAUSED
##mode at the desired current or field.
##3. Record the desired current or field setting.
##4. Deactivate the switch heater control (the LED indicator should
##extinguish).
##5. Wait until the switch heater is completely cooled before changing
##any parameters. Most persistent switches cool to superconducting
##state in a few seconds if completely submerged in liquid helium.
##6. Once the switch has cooled, the Model 420 may be used to ramp the
##current to zero at an increased ramp rate (since the magnet is no
##longer in the circuit). Using the ZERO mode is recommended since
##it allows the programmed current/field to remain unchanged for
##future sessions.
##7. Once at zero current, de-energize the power supply first, then
##power-off the Model 420 instrument.
    
#############################################    
##3.4.2 Procedure for Exiting Persistent Mode
##To exit the persistent mode of magnet operation, the operator should
##perform the following steps:
##1. If the Model 420 has been powered-off, then first energize the
##Model 420. After the Model 420 has been energized, energize the
##power supply.
##2. Using the value of current or field recorded when the magnet last
##entered the persistent mode, use either the programmed or manual
##ramping modes of the Model 420 to achieve the last recorded value
##of current or field.
##3. The Model 420 should be either in the HOLDING or PAUSED
##mode at the last recorded value of current or field.
##4. Activate the switch heater control (the LED indicator should
##illuminate). Note that the Model 420 will enter the HEATING
##Rev. 7 61
##Operation
##Quench Detection
##SWITCH mode and disallow any ramping during the switch
##heating period.
##5. Once the switch heating period expires, the Model 420 will enter
##the PAUSED mode and will maintain the operating current or
##field.
##Note
##If the actual current in the magnet and the operating current of the
##Model 420 exhibit a mismatch at the time the switch heater is
##activated, the Model 420 will track the actual current of the magnet
##during the switch heating period. At the expiration of the switch
##heating period, the Model 420 will attempt to maintain the last
##measured current value.

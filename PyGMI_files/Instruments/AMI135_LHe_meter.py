# -*- coding: utf-8 -*-
import visa,time
# Retry decorator with return
def retry_with(tries=2,ans_type=int,default_ans=-1,wait=1):
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
                    success=False
                    mtries -= 1      # consume an attempt
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
                    success=False
                    mtries -= 1      # consume an attempt
                    time.sleep(wait)
            if not(success):
                print "ran out of retries: exception with function", f.func_name
        return f_retry # true decorator -> decorated function
    return deco_retry  # @retry(arg[, ...]) -> true decorator

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::1"):
        #part to be run at instrument initialization, the following commands are mandatory
        self.io = visa.ResourceManager().open_resource(VISA_address)
        self.VISA_address=VISA_address
        print self.query_unit_Id()

    #mandatory function
    #return instrument identification. This command is common to almost all GPIB instruments. Modify if necessary.
    def query_unit_Id(self):
        return"AMI135 LHe meter does not implement *IDN?"
        #return self.io.query("*IDN?") 

    #mandatory function that will be called just after the computer successfully connected to the instrument.
    #If you don't need it, just leave it empty but do leave the command "return 1"
    def initialize(self):
        ####your initialization commands
        ####
        return 1        

    #define the functions that you want accessible in your measurements program for that type of instrument
    def query_unit(self):
        translation={"%":"%","C":"cm","I":"inches"}
        self.io.write("UNIT")
        self.io.wait_for_srq()
        res=self.io.read()
        if translation.has_key(res):
            return translation[res]
        else:
            return res

    def set_unit_to_percent(self):
        self.io.write("PERCENT")
        self.io.wait_for_srq()
        res=self.io.read()
        #there is an error in the manual: this command actually returns "PERCENT" and not "%"
        if res=="PERCENT": 
            return 1
        else:
            return 0
        
    def set_unit_to_cm(self):
        self.io.write("CM")
        self.io.wait_for_srq()
        res=self.io.read()
        if res=="CM":
            return 1
        else:
            return 0
        
    def set_unit_to_inches(self):
        self.io.write("INCH")
        self.io.wait_for_srq()
        res=self.io.read()
        if res=="INCH":
            return 1
        else:
            return 0

    def query_LHe_level(self):
        self.io.write("LEVEL")
        self.io.wait_for_srq()
        res=self.io.read()
        return res+self.query_unit()

    @retry_with(tries=2,ans_type=float,default_ans=-1,wait=1)
    def query_LHe_level_in_pct(self):
        self.set_unit_to_percent()
        self.io.write("LEVEL")
        self.io.wait_for_srq()
        res=self.io.read()
        return float(res)

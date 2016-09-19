# -*- coding: utf-8 -*-
import visa
import re
import numpy as np
import time

Regexfloat = "([-+]?(?:\d+\.?\d*|\.\d+)(?:[eE][-+]?\d+)?)"
LRanswer = re.compile(Regexfloat+r' (K| |M|U)OHM (?:/\\X|/\\R|10/\\R|10/\\X|R|X|RSET|XSET) *\n')
LRstat = re.compile(r'(\d)R,(\d)E,(\d+)\%,(\d)F(?:\( ?'+Regexfloat+r' (s|M)\))?,(\d)M,(\d)L,(\d\d)S\n')
# TODO: 'U' definitely indicated microOhm in my experiment
# but Adam said it's also the symbol for megaOhm ?
LRmultconv = {'U':1e-6,'M':1e-3,' ':1e0,'K':1e3}
LRfiltconv = {'s':1.0,'M':60.0}

def LRreader(x):
    match = LRanswer.match(x)
    if match is not None:
        res = float(match.group(1))*LRmultconv[match.group(2)]
    else:
        res = 1e99
    return res
      
    
LRrange = {0:'2 mOhm',
           1:'20 mOhm',
           2:'200 mOhm',
           3:'2 Ohm',
           4:'20 Ohm',
           5:'200 Ohm',
           6:'2 kOhm',
           7:'20 kOhm',
           8:'200 kOhm',
           9:'2 MOhm'}

LRran = np.array([2e-3,20e-3,200e-3,2,20,200,2e3,20e3,200e3,2e6])

LRexcitation = {0:'20 uV',
                1:'60 uV',
                2:'200 uV',
                3:'600 uV',
                4:'2 mV',
                5:'6 mV',
                6:'20 mV'}

LRexc = np.array([20e-6,60e-6,200e-6,600e-6,2e-3,6e-3,20e-3])

LRfilter = {0:'1 sec',
            1:'3 sec',
            2:'10 sec',
            3:'variable filter'}
            
LRvarfilter = np.concatenate((np.array([0.2,0.4,0.6,0.8,
                                        1.0,1.6,2.0,3.0,5.0,7.0,
                                        10.0,15.0,20.0,30.0,45.0]),
                                        np.array([1.0,1.5,2.0,3.0,5.0,7.0,
                                                  10.0,15.0,20.0,30.0])*60.0))
               
LRmode = {0:'x1 mode (1 Delta R)',1:'x10 mode (10 Delta R)'}
LRlockout = {0:'Front panel unlocked',1:'Front panel locked'}

    
class Connect_Instrument():
    def __init__(self,VISA_address="GPIB1::18::INSTR"):
        self.io = visa.ResourceManager().open_resource(VISA_address)

    def initialize(self):
        return 1      
        
    def query_unit_Id(self):
        return "This instrument does not implement *IDN?"
    
    def query_R(self):
        return LRreader(self.io.query("get 0",delay=0.1))

    def query_dR(self):
        return LRreader(self.io.query("get 2",delay=0.1))

    def query_dX(self):
        return LRreader(self.io.query("get 3",delay=0.1))        

    def query_X(self):
        return LRreader(self.io.query("get 1",delay=0.1))
        
    def query_RSET(self):
        return LRreader(self.io.query("get 4",delay=0.1))   

    def query_XSET(self):
        return LRreader(self.io.query("get 5",delay=0.1))           

    def set_mode(self,txt):
        """
        '1x' or '10x'
        in '10x' mode only 10% variations from the RSET=R value is measurable
        """
        conv = {'1x':'0','10x':'1'}
        self.io.write('M '+conv[txt])
        
    def set_offset(self,txt):
        """
        'zero' or 'RSET=R and XSET=X'
        null the offset, or set the offset to the current R and X values
        """        
        conv = {'zero':'=0','RSET=R and XSET=X':'=R'}
        self.io.write('O '+conv[txt])
        
    def set_excitation(self,value):
        """
        Set the LR700 excitation to the closest setting inferior or equal
        to 'value' (in V) or to 20 uV, whichever is larger
        """
        if type(value)==float:
            if value<=20e-6:
                res = 0
            else:
                # find the largest 'excitation' inferior to 'value'
                res = np.arange(0,7,1)[LRexc<=value][-1]
            self.io.write('E '+str(res))
            time.sleep(0.1)
            self.io.write('V 0')
        else:
            raise TypeError

    def set_varexcitation(self,value):
        """
        'value' in volts (2uV to 20mV)
        The LR700 allows discrete voltage steps, in percentage of 
        7 ranges, from 20 uV to 20mV.
        This finds the voltage closest to 'value', rounded to 
        the lower integer percentage
        """
        # find the smallest excitation range higher than 'value'
        if value > 20e-3:
            res = 6
            pct = 100
        else:
            res = np.arange(0,7,1)[LRexc>=value][0]
            pct = int(value/LRexc[res]*100)
            if pct < 5:pct = 5

        if pct == 100:
            self.io.write('E '+str(res))
            time.sleep(0.1)            
            self.io.write('V 0')
        else:
            # note that for a short period of time
            # the excitation will be some pctage of the previously selected
            # range which may or may not damage the sample
            self.io.write('V 1')
            time.sleep(0.1)
            self.io.write('V ='+str(pct).zfill(2))
            print 'V ='+str(pct).zfill(2)
            time.sleep(0.1)
            self.io.write('E '+str(res))

    def set_range(self,value):
        """
        'value' in Ohm (2mOhm to 2MOhm)
        Set the LR700 range to the closest setting superior to 'value'
        or to 2 MOhm, whichever is smaller
        """
        if type(value)==float:
            if value>=2e6:
                res = 9
            else:
                # find the smallest 'range' superior to 'value'
                res = np.arange(0,10,1)[LRran>=value][0]
            self.io.write('R '+str(res))
        else:
            raise TypeError
        
    def set_time_cste(self,value):
        """
        value in seconds (0.2 to 1800 s)
        The LR700 takes a datapoint every 188 ms.
        This tells it how long to average internally.
        It only allows discrete duration steps,
        so this finds the longest time constant lower than 'value'
        """
        conv = {1.0:'0',3.0:'1',10.0:'2'}
        if conv.has_key(value):
            # 1, 3 and 10 have a special setting just for themselves
            self.io.write('F '+conv[value])
        else:
            # find the largest time constant inferior to 'value'
            if value <0.2:
                res = 0
            else:
                res = np.arange(0,25,1)[LRvarfilter<=value][-1]
            self.io.write('F 3')
            time.sleep(0.1)
            self.io.write('F ='+str(res).zfill(2))
            
        
    def query_bridge_setting(self,verbose=False):
        ans = self.io.query('get 6',delay=0.1)
        stats = {}
        match = LRstat.match(ans)
        if match is not None:
            stats['range'] = int(match.group(1))
            stats['excitation'] = int(match.group(2))
            stats['pct excitation'] = int(match.group(3))
            stats['filter'] = int(match.group(4))
            if stats['filter'] == 3:
                stats['vartime'] = float(match.group(5))*LRfiltconv[match.group(6)]
            #NB: the groups numbering has the good taste of including optional argument
            stats['mode'] = int(match.group(7))
            stats['lockout'] = int(match.group(8))
            stats['sensor'] = int(match.group(9))       
            if verbose:
                stats['range_txt'] = LRrange[stats['range']]
                stats['excitation_txt'] = LRexcitation[stats['excitation']]
                stats['filter_txt'] = LRfilter[stats['filter']]
                stats['mode_txt'] = LRmode[stats['mode']]
                stats['lockout_txt'] = LRlockout[stats['lockout']]
        else:
            stats = ans
        return stats

    def query_bridge_current(self):
        """
        Return the constant AC current actually used by the bridge
        for this specific range and excitation voltage
        (It is simply excitation voltage/resistance range)
        """
        stats = self.query_bridge_setting(verbose=False)        
        return (LRexc[stats['excitation']]*stats['pct excitation']/100.0)/LRran[stats['range']]        
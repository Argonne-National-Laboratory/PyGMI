# -*- coding: utf-8 -*-
import visa
import numpy as np

LSVRANGE = {1: '2.00 μV', 2: '6.32 μV', 3: '20.0 μV', 4: '63.2 μV',
            5: '200 μV', 6: '632 μV', 7: '2.0 mV', 8: '6.32 mV'}

LSVRAN = np.array([2e-6,6.32e-6,20e-6,63.2e-6,200e-6,632e-6,
                   2e-3,6.32e-3])

LSIRANGE = {1: '1.00 pA', 2: '3.16 pA', 3: '10.0 pA', 4: '31.6 pA',
            5: '100 pA', 6: '316 pA', 7: '1.00 nA', 8: '3.16 nA',
            9: '10.0 nA', 10: '31.6 nA', 11: '100 nA', 12: '316 nA',
            13: '1.00 μA', 14: '3.16 μA', 15: '10.0 μA', 16: '31.6 μA',
            17: '100 μA', 18: '316 μA', 19: '1.00 mA', 20: '3.16 mA',
            21: '10.0 mA', 22: '31.6 mA'}

LSIRAN = np.array([1e-12,3.16e-12,10e-12,31.6e-12,100e-12,316e-12,
                   1e-9,3.16e-9,10e-9,31.6e-9,100e-9,316e-9,
                   1e-6,3.16e-6,10e-6,31.6e-6,100e-6,316e-6,
                   1e-3,3.16e-3,10e-3,31.6e-3])

LSRRANGE = {1: '2.0 mOhm', 2: '6.32 mOhm', 3: '20.0 mOhm', 4: '63.2 mOhm',
            5: '200 mOhm', 6: '632 mOhm', 7: '2.00 Ohm', 8: '6.32 Ohm',
            9: '20.0 Ohm', 10: '63.2 Ohm', 11: '200 Ohm', 12: '632 Ohm',
            13: '2.00 kOhm', 14: '6.32 kOhm', 15: '20.0 kOhm', 16: '63.2 kOhm',
            17: '200 kOhm', 18: '632 kOhm', 19: '2.00 MOhm', 20: '6.32 MOhm',
            21: '20.0 MOhm', 22: '63.2 MOhm'}

LSRRAN = np.array([2e-3,6.32e-3,20e-3,63.2e-3,200e-3,632e-3,
                   2e-0,6.32e-0,20e-0,63.2e-0,200e-0,632e-0,
                   2e+3,6.32e+3,20e+3,63.2e+3,200e+3,632e+3,
                   2e+6,6.32e+6,20e+6,63.2e+6,200e+6,632e+6
                   ])

class Connect_Instrument():
    def __init__(self,VISA_address="GPIB0::12"):
        self.io = visa.ResourceManager().open_resource(VISA_address)
        print(self.query_unit_Id())
        self.delay = 0.1

    def initialize(self,combobox=None):
        pass

    def query_unit_Id(self):
        return self.io.query("*IDN?")

    def query_temp(self,channel):
        #reports the current temperature reading on any of the input channels
        #channel can be A,B,C,D
        return float(self.io.query("KRDG? "+channel))

    def query_R(self,channel):
        """
        Sensor Reading Query, always in ohms
        "channel" Specifies which  channel to query:
            A -> control input
            1 to 16 -> measurement input
        """
        return float(self.io.query("SRDG?"+str(channel),delay=self.delay))

    def query_X(self,channel):
        return float(self.io.query("QRDG?"+str(channel),delay=self.delay))

    def query_frequency(self, channel='measure'):
        """
        Return control or measurement frequency in Hertz (default measurement)
        """
        trans = {'measure':'0','control':'A'}
        conv = {1: 9.8, 2: 13.7, 3: 16.2, 4: 11.6, 5: 18.2}
        return conv[int(self.io.query("FREQ?"+trans[channel],delay=0.1))]

    def set_frequency(self, channel='measure', freq=13.7):
        """
        Set control or measurement frequency in Hertz (default measurement)
        """
        trans = {'measure':'0','control':'A'}
        conv = {9.8: '1', 13.7: '2', 16.2: '3', 11.6: '4', 18.2: '5'}
        if freq in conv:
            self.io.write("FREQ"+trans[channel]+','+conv[freq],delay=10)
        else:
            print('frequency',freq,'Hz not available')
            raise ValueError

    def set_Input_Channel_Parameter(self, channel, enable, dwell, pause,
                                    curvenb=0, tempcoeff='positive'):
            conv = {'positive': 2, 'negative': 1}
            self.io.write("INSET "+str(channel)+','+str(int(enable))+','+\
                          str(dwell)+','+str(pause)+','+str(curvenb)+','+\
                          str(conv[tempcoeff]),
                          delay=0.1)

    def get_Input_Channel_Parameter(self, channel):
         enable, dwell, pause, curvenb, tempcoeff \
         = self.io.query("INSET?"+str(channel))
         conv = {2: 'positive', 1: 'negative'}
         return bool(enable), dwell, pause, curvenb, conv[tempcoeff]

    def set_Input_Setup(self, channel, mode, excitation, autorange, res_range,\
                        cs_shunt, units):
        """
        Set the LS372 excitation to the closest setting inferior or equal
        to 'excitation' (in V or A)
        Set the LS372 range to the closest setting superior to 'res_range'

        """
        conv0 = {'voltage source': 0, 'current source': 1}
        conv1 = {'source on': 0, 'source off': 1}
        conv2 = {'kelvin': 1, 'ohms': 2}
        convauto = {'auto on': 1, 'auto off': 0}

        if conv0[mode]:
            # find the largest current inferior to 'excitation'
            if excitation <= 1e-12:
                ran = 1
            else:
                ran = np.arange(0,len(LSIRAN),1)[LSIRAN <= excitation][-1] + 1
        else:
            # find the largest voltage inferior to 'excitation'
            if excitation <= 2e-6:
                ran = 1
            else:
                ran = np.arange(0,len(LSVRAN),1)[LSVRAN <= excitation][-1] + 1

        # find the smallest 'range' superior to 'res_range'
        if res_range >= 63.2e6:
            res_ran = 22
        else:
            res_ran = np.arange(0,len(LSRRAN),1)[LSRRAN >= res_range][0] + 1

#        self.io.write(
        print("INTYPE "+str(channel)+','+str(conv0[mode])+','+\
                          str(ran)+','+str(convauto[autorange])+','+str(res_ran)\
                          +','+str(conv1[cs_shunt])+','+str(conv2[units]))
#                          ,delay=0.1)

    def query_Input_Setup(self, channel, verbose=False):
        ans = self.io.query('INTYPE?'+str(channel), delay=0.1).split(',')

        conv0 = {0: 'voltage source', 1: 'current source'}
        conv1 = {0: 'source on', 1: 'source off'}
        conv2 = {1: 'kelvin', 2: 'ohms'}
        convauto = {1: 'auto on', 0: 'auto off'}

        stats = {}
        if verbose:
            stats['mode'] = conv0[int(ans[0])]
            if int(ans[0]):
                stats['excitation'] = LSIRAN[int(ans[1])-1]
                stats['excitation_txt'] = LSIRANGE[int(ans[1])]
            else:
                stats['excitation'] = LSVRAN[int(ans[1])-1]
                stats['excitation_txt'] = LSVRANGE[int(ans[1])]
            stats['autorange'] = convauto[int(ans[2])]
            stats['range'] = LSRRAN[int(ans[3])-1]
            stats['range_txt'] = LSRRANGE[int(ans[3])]
            stats['source'] = conv1[int(ans[4])]
            stats['units'] = conv2[int(ans[5])]
        else:
            stats['mode'] = int(ans[0])
            stats['excitation'] = int(ans[1])
            stats['autorange'] = int(ans[2])
            stats['range'] = int(ans[3])
            stats['source'] = int(ans[4])
            stats['units'] = int(ans[5])

        return stats

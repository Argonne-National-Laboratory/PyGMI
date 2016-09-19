# If you want a value of the frontpanel to be accessible for use in a measurements program it has to be
# added in here
# 
# Example: suppose we just added a text entry in the interface (the .ui file) using Qt Designer
# We named that entry "my_text_entry" in Qt Designer
# This entry can now be accessed from here using the name "ui.my_text_entry"
# Next, we want to retrieve the text in that entry and put it in the variable "my_text",
# for that we just add the line "self.my_text=ui.my_text_entry.text()" 
# In the measurement scripts, self.my_text will be accessible as f.my_text

import re
import numpy as np

class Frontpanel_values():
    def __init__(self,ui):
        #################
        #"Instr I/O" tab#
        #################
        #CHECKBOXES next to the instruments adresses
        for chb in ui.instr_IO.list_of_all_checkboxes_pointer():
            #print chb.objectName()
            exec("self."+chb.objectName()+"="+str(chb.isChecked()))
        #Text entries
        self.channels_list_1=ui.instr_IO.ui.channels_list_1.text().split(',')
        self.channels_list_2=ui.instr_IO.ui.channels_list_2.text().split(',')
        self.mapping=ui.instr_IO.ui.mapping.text().split(',')
        
        ####################
        #"Measurements" tab#
        ####################
        #Text entries
        self.email_address=ui.email_address.text()
        self.savefile_txt_input=ui.savefile_txt_input.text()
        
        #Numeric entries
        self.mesure_delay=ui.mesure_delay.value()/1000.0
        self.mesure_speed=ui.mesure_speed.value()
        self.repeat_points=ui.repeat_points.value()
        
        self.current1=ui.I_source_setpoint.value()*1e-6
        self.current2=ui.I_source_setpoint_2.value()*1e-6
        self.current3=ui.I_source_setpoint_3.value()*1e-6

        self.voltage1=ui.V_setpoint_1.value()
        self.voltage2=ui.V_setpoint_2.value()
        self.voltage3=ui.V_setpoint_3.value()

        self.IV_voltage_criterion=ui.IV_voltage_criterion.value()*1e-6

        self.B_X_setpoint=ui.B_X_setpoint.value()
        self.B_Y_setpoint=ui.B_Y_setpoint.value()
        self.B_Z_setpoint=ui.B_Z_setpoint.value()

        self.anglestart=ui.anglestart.value()
        self.anglestop=ui.anglestop.value()
        self.anglestep=ui.anglestep.value()
        
        #CHECKBOXES
        self.voltage_criterion_on=ui.voltage_criterion_on.isChecked()
                
        #Tables       
        #####Temperature
##        self.min_T=[]
##        self.step_T=[]
##        self.max_T=[]
##        #self.T_rate=[]
##        self.Temp_table_length=ui.Temp_table.ui.table.rowCount()
##        for i in range(self.Temp_table_length):
##            if type(ui.Temp_table.ui.table.item(i,0))!=type(None):
##                self.min_T.append(float(ui.Temp_table.ui.table.item(i,0).text()))
##                self.step_T.append(float(ui.Temp_table.ui.table.item(i,1).text()))
##                self.max_T.append(float(ui.Temp_table.ui.table.item(i,2).text()))
##                #self.T_rate.append(float(ui.Temp_table.ui.table.item(i,3).text()))
##        self.temps_list=[]
##        for i in range(len(self.min_T)):
##            if self.max_T[i]>self.min_T[i]:self.temps_list.extend([self.min_T[i]+j*abs(self.step_T[i]) for j in range(int((self.max_T[i]-self.min_T[i])/abs(self.step_T[i])))])
##            if self.max_T[i]<=self.min_T[i]:self.temps_list.extend([self.min_T[i]-j*abs(self.step_T[i]) for j in range(int(-(self.max_T[i]-self.min_T[i])/abs(self.step_T[i])))])
        

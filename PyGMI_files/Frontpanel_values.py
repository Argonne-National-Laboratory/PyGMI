# If you want a value of the front panel to be accessible for use in a
# measurements program it has to be added in here
#
# Example: suppose we just added a text entry in the interface (the .ui file)
# using Qt Designer
# We named that entry "my_text_entry" in Qt Designer
# This entry can now be accessed from here using the name "ui.my_text_entry"
# Next, we want to retrieve the text in that entry and put it in the variable "my_text",
# for that we just add the line "self.my_text=ui.my_text_entry.text()"
# In the measurement scripts, self.my_text will be accessible as f.my_text

#import re
#import numpy as np

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

        #LR700
        LR700rangelist = [2e-3,20e-3,200e-3,2,20,200,2e3,20e3,200e3,2e6]
        self.range_LR700 = LR700rangelist[ui.range_LR700.currentIndex()]
        self.integ_rate_LR700 = ui.integ_rate_LR700.value()
        self.V_LR700 = ui.V_LR700.value()*1e-6

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

        self.B_start=ui.B_X_setpoint.value()
        self.B_stop=ui.B_Y_setpoint.value()
        self.B_step=ui.B_Z_setpoint.value()

        self.anglestart=ui.anglestart.value()
        self.anglestop=ui.anglestop.value()
        self.anglestep=ui.anglestep.value()

        #CHECKBOXES
        self.voltage_criterion_on=ui.voltage_criterion_on.isChecked()

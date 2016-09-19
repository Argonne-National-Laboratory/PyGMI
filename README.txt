2016/09/09 Major update
Master branch was designed for the latest version of Python 2 and use PySide
New beta release (branch "v3-beta") was adapted to work with PyQt and so it should now work with Spyder (in the spyder console subwindow, select using the "console" tab, not the "IPython console" tab)
v3-beta updates:
-switched to PyQt and Spyder
-adapted to Pyvisa >1.5 (rough patch provided in main folder to update old instruments drivers)
-include a new ppms driver and Macro commands to control the ppms. But to get this feature to work you need to download the "QDInstrument.dll" from the Pharos website of Quantum Design and place it in the folder : PyGMI_files\Instruments\MyPPMSDLL\data


Welcome to PyGMI ! What is PyGMI ?
PyGMI is an open source Generic Measurements Interface made in Python/Qt that can take measurements with instruments connected over GPIB, RS232, ethernet or USB using Pyvisa and PySerial. It features:
•	live display of the data acquired using pyqtgraph
•	a macro editor that can make a series of mesurements and even send e-mails with data! 
•	generic instruments panels, that can easily be created for a class of instruments using using the WYSIWYG interface designer QtDesigner
•	a graphical interface that can also be easily modified using QtDesigner
•	a main configuration panel that can store instruments types and instruments addresses for easy reconfiguration from one experiment to the next
•	measurements that are taken in a separate process so that they do not burden the graphical interface
•	generic python drivers can easily be created for new instruments
Its philosophy is that acquiring data with instruments, displaying it live and saving these data is a very generic thing, whereas the core of an experiment is: what instruments do what and in which order. Therefore, PyGMI provides a framework that relieves the user from doing all those generic tasks, so that taking measurements become as simple as writing “what instruments do what and in which order” such as :

currentsource.set_current_amplitude(+I)
Vp=voltmeter.query_voltage()
currentsource.set_current_amplitude(-I)
Vm=voltmeter.query_voltage()

Check out the documentation for more details !

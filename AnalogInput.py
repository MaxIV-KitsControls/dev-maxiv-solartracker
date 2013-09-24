import sys
import time

import PyTango

import Adafruit_BBIO.ADC as ADC

class AnalogInput(PyTango.Device_4Impl):
    
    AI1_PIN = 'P9_40'
    AI2_PIN = 'P9_38'
    AI3_PIN = 'P9_36'

    def __init__(self, devclass, name):
        PyTango.Device_4Impl.__init__(self, devclass, name)
        self.init_device()

    def delete_device(self):
	pass
    
    def init_device(self):
        self.get_device_properties()
	ADC.setup()
    
    def read_Channel1(self, attr):
	reading = ADC.read(AnalogInput.AI1_PIN)
	volts = reading * 1.800
        attr.set_value(volts)
        
    def read_Channel2(self, attr):
	reading = ADC.read(AnalogInput.AI2_PIN)
	volts = reading * 1.800
        attr.set_value(volts)

    def read_Channel3(self, attr):
	reading = ADC.read(AnalogInput.AI3_PIN)
	volts = reading * 1.800
        attr.set_value(volts)

class AnalogInputClass(PyTango.DeviceClass):
    
    class_property_list = {}

    device_property_list = {
#        'host':
#            [PyTango.DevString, "host of power supply", "localhost"],
    }

    cmd_list = {
#        'ramp':
#            [ [PyTango.DevVoid, "nothing"],
#              [PyTango.DevVoid, "nothing"] ],
    }

    attr_list = {
        'Channel1':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            { 'label' : 'Channel 3', 'unit' : 'Volt' }],
        'Channel2':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            { 'label' : 'Channel 3', 'unit' : 'Volt' }],
        'Channel3':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ],
            { 'label' : 'Channel 3', 'unit' : 'Volt' }],
    }
    

def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(AnalogInputClass,AnalogInput,'AnalogInput')

        U = PyTango.Util.instance()
        U.server_init()
        U.server_run()

    except PyTango.DevFailed,e:
        print '-------> Received a DevFailed exception:',e
    except Exception,e:
        print '-------> An unforeseen exception occured....',e

def trace(frame, event, arg):
    print "%s, %s:%d" % (event, frame.f_code.co_filename, frame.f_lineno)
    return trace


if __name__ == "__main__":
#    sys.settrace(trace)
    main()

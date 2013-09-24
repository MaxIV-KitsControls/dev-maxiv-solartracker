import sys
import time

import PyTango

import Adafruit_BBIO.PWM as PWM

class ServoMotor(PyTango.Device_4Impl):
    
    #SENSOR_PIN = 'P9_40'
    SENSOR_PIN = 'P9_38'
    #SENSOR_PIN = 'P9_36'
    PAN_SERVO_PIN  = "P9_14"
    TILT_SERVO_PIN  = "P8_19"
    duty_min = 3
    duty_max = 14.5
    duty_span = duty_max - duty_min

    def __init__(self, devclass, name):
        PyTango.Device_4Impl.__init__(self, devclass, name)
        self.init_device()

    def delete_device(self):
        PWM.stop(self.PWM_PIN)
        PWM.stop(self.PWM_PIN)
        PWM.cleanup()

    
    def init_device(self):
        self.get_device_properties()
        self.position = 0
	PWM.start(self.PWM_PIN, (100 - ServoMotor.duty_min), 60.0, 1)
    
    def read_Position(self, attr):
        attr.set_value_date_quality(self.position, time.time(), PyTango.AttrQuality.ATTR_WARNING)
    
    @PyTango.DebugIt()
    def write_Position(self, attr):
        self.position = attr.get_write_value()
        duty = 100 - ((self.position / 180) * ServoMotor.duty_span + ServoMotor.duty_min)
	#PWM.start(ServoMotor.TILT_SERVO_PIN, duty, 60.0, 1)
	PWM.set_duty_cycle(self.PWM_PIN, duty)


class ServoMotorClass(PyTango.DeviceClass):
    
    class_property_list = {}

    device_property_list = {
        'PWM_PIN': [PyTango.DevString, "pwm signal pin out", ""],
    }

    cmd_list = {
#        'ramp':
#            [ [PyTango.DevVoid, "nothing"],
#              [PyTango.DevVoid, "nothing"] ],
    }

    attr_list = {
        'Position':
            [[PyTango.DevDouble,
            PyTango.SCALAR,
            PyTango.READ_WRITE], 
            { 'label' : 'Position', 'unit' : 'deg' }],
    }
    

def main():
    try:
        py = PyTango.Util(sys.argv)
        py.add_class(ServoMotorClass,ServoMotor,'ServoMotor')

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

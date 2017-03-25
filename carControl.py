import serial , time
import serial.tools
import serial.tools.list_ports
import os
class carControl:

    def __init__(self):

        # directions are 'F' 'U' 'L' 'R'
        arduino_ports = [
            p.device
            for p in serial.tools.list_ports.comports()
            if 'Arduino' in p.description
            ]
        if not arduino_ports:
            raise IOError("No Arduino found")
        path = arduino_ports[0]
        mod = 777
        #os.chmod(path, mod);
        self.carSerial = serial.Serial(path)
        self.direction = 'F'

    def moveCar(self, command):
        FORWARD = 1
        REVERSE = 2
        STOP = 0
        if (command == STOP):
            self.carSerial.write('s'.encode())
        if (command == FORWARD):
            self.carSerial.write('f'.encode())
        if (command == REVERSE):
            self.carSerial.write('r'.encode())

        return

    def drive(self,spd):
        if (spd > 0):
            self.moveCar(1)
        return

    def stop(self, dst):
        self.moveCar(0)
        return



cntrl = carControl()
cntrl.drive()
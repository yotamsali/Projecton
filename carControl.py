import serial , time
class carControl:
    def __init__(self):
        # directions are 'F' 'U' 'L' 'R'
        self.carSerial = serial.Serial(port='/dev/ttyACM0')
        time.sleep(1)
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





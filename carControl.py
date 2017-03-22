import serial , time
class carControl:
    def __init__(self):
        # directions are 'F' 'U' 'L' 'R'
        self.carSerial = serial.Serial(port='COM14')
        time.sleep(1)
        self.direction = 'F'

    def moveCar(command, self):
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
        elif (spd < 0):
            self.moveCar(2)
        else:
            self.moveCar(0)
        return

a = carControl()
a.moveCar(1)




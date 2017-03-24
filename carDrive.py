import serial , time

#initializes the connection with car and returns the serial port
def init():
    carSerial = serial.Serial(port='COM3')
    time.sleep(1)
    return carSerial


## get a command and the serial port of the car and transfers the instruction
## to the car. 1 for forward , 2 for reverse and 0 for stop
def moveCar(command , carSerial ) :
    FORWARD = 1
    REVERSE = 2
    STOP = 0
    if (command == STOP):
        carSerial.write('s'.encode())
    if (command ==FORWARD ):
        carSerial.write('f'.encode())
    if (command == REVERSE):
        carSerial.write('r'.encode())


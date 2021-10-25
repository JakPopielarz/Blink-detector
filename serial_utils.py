import serial

class Serial(serial.Serial):
    def __init__(self, com_port, baud):
        super().__init__(port=com_port, baudrate=baud, 
            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.received = ""

    def receive(self):
        while(1):
            # Wait until there is data waiting in the serial buffer
            if(self.in_waiting > 0):
                # Read data out of the buffer until a carraige return / new line is found
                self.received = self.readline()
                # Print the contents of the serial data
                print(self.received.decode('Ascii'))

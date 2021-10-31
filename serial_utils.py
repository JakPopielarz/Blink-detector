import serial
import threading

from serial.serialutil import SerialException

class Serial(serial.Serial):
    def __init__(self, com_port, baud, data_max_count=1000):
        try:
            super().__init__(port=com_port, baudrate=baud, 
                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        except SerialException:
            print("Couldn't open serial port " + self.port + ". Maybe the device isn't connected?")

        self.received = [0 for _ in range(data_max_count)]
        self.data_max_count = data_max_count
        self.receiving_thread = None
        self.__do_receive = False

    """
    Receive data from a specified serial port.
    Save the decoded & cast to int signal to list of received data
    """
    def start_receiving(self):
        if self.isOpen() and not self.__do_receive:
            self.__do_receive = True
            self.receiving_thread = threading.Thread(target=self.__receive, daemon=True)

            print("Starting data receiving")
            self.receiving_thread.start()
        else:
            print("Couldn't start receiving data on serial port " + self.port + ". Try setting a different port.")

    def __receive(self):
        try:
            while(self.__do_receive):
                # Wait until there is data waiting in the serial buffer
                if(self.in_waiting > 0):
                    # Read data out of the buffer until a carraige return / new line is found
                    received_value= self.readline()
                    # Print the contents of the serial data
                    self.__save_data(self.__decode(received_value))
        except SerialException:
            print("Something went wrong while receiving data from " + self.port + ". Shutting down.")

    """
    Decode the value passed as argument & cast it to int
    """
    def __decode(self, value):
        return int(value.decode('Ascii'))

    """
    Add the value to end of list of received data.
    If length of the list is bigger than specified on init - pop first element
    """
    def __save_data(self, value):
        self.received.append(value)

        if len(self.received) > self.data_max_count:
            self.received.pop(0)
    
    def stop_receiving(self):
        if self.__do_receive:
            print("Stopping data receiving")
            self.__do_receive = False
            self.receiving_thread.join()

    def get_received(self):
        return self.received

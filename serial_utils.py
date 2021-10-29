import serial
import threading

class Serial(serial.Serial):
    def __init__(self, com_port, baud, data_max_count=1000):
        super().__init__(port=com_port, baudrate=baud, 
            bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        self.received = []
        self.data_max_count = data_max_count
        self.receiving_thread = None
        self.__do_receive = False

    """
    Receive data from a specified serial port.
    Save the decoded & cast to int signal to list of received data
    """
    def start_receiving(self):
        self.__do_receive = True
        self.receiving_thread = threading.Thread(target=self.__receive, daemon=True)

        print("Starting data receiving")
        self.receiving_thread.start()

    def __receive(self):
        while(self.__do_receive):
            # Wait until there is data waiting in the serial buffer
            if(self.in_waiting > 0):
                # Read data out of the buffer until a carraige return / new line is found
                received_value= self.readline()
                # Print the contents of the serial data
                self.__save_data(self.__decode(received_value))
                print(self.received)

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
        print("Stopping data receiving")
        self.__do_receive = False
        self.receiving_thread.join()

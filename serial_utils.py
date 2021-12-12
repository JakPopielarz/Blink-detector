import serial
import threading
import time

from serial.serialutil import SerialException

class Serial(serial.Serial):
    def __init__(self, com_port, baud, data_max_count=1000):
        try:
            super().__init__(port=com_port, baudrate=baud, 
                bytesize=8, timeout=2, stopbits=serial.STOPBITS_ONE)
        except SerialException:
            pass

        self.received = [-100] * data_max_count
        self.data_max_count = data_max_count
        self.receiving_thread = None
        self.receiving = False
        self.error_in_receiving = False
        self.triggered = False
        self.mock = False # For testing purposes only
        self.count = 0

    def start_receiving(self):
        """
        Receive data from a specified serial port.
        Save the decoded & cast to int signal to list of received data
        Returns bool indicating if succededd
        """
        try:
            if not self.mock:
                self.open()
        except SerialException:
            pass

        if self.isOpen() and not self.receiving and not self.mock:
            self.receiving = True
            self.receiving_thread = threading.Thread(target=self.__receive, daemon=True)

            self.receiving_thread.start()
        elif not self.receiving and self.mock: # For testing purposes only
            self.receiving = True
            self.receiving_thread = threading.Thread(target=self.__mock_receive, daemon=True)
            self.receiving_thread.start()
        else:
            self.__save_data(0)

    def __receive(self):
        try:
            while(self.receiving):
                # Wait until there is data waiting in the serial buffer
                if(self.in_waiting > 0):
                    # Read data out of the buffer until a carraige return / new line is found
                    received_value = self.readline()
                    # Save the contents of the serial data
                    self.__save_data(self.__decode(received_value))
                    self.count += 1
        except SerialException:
            self.error_in_receiving = True

    def __mock_receive(self):
        """
        For testing purposes only
        """
        try:
            modifier = 1
            step = 3
            while(self.receiving):
                if self.received[-1] > 700:
                    modifier *= -1
                    mock_data = self.received[-1] - 2*step
                elif self.received[-1] < 200:
                    modifier *= -1
                    mock_data = self.received[-1] + 2*step
                else:
                    mock_data += step * modifier
                self.__save_data(mock_data)
                time.sleep(0.05)
        except:
            self.error_in_receiving = True

    def __decode(self, value):
        """
        Decode the value passed as argument & cast it to int
        """
        try:
            return int(value.decode('Ascii').strip())
        except:
            return -100

    def __save_data(self, value):
        """
        Add the value to end of list of received data.
        If length of the list is bigger than specified on init - pop first element
        """
        self.received.append(value)

        if len(self.received) > self.data_max_count:
            self.received.pop(0)
    
    def stop_receiving(self):
        if self.receiving:
            self.close()
            self.receiving = False
            self.receiving_thread.join()

    def get_received(self):
        return self.received

    def get_received_delta(self):
        points_count = self.count
        self.count = 0
        if points_count == 0:
            return []
        return self.received[-points_count:]

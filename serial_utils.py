import serial
import threading
import time

from serial.serialutil import SerialException

class Serial(serial.Serial):
    """
    Serial communication tool class. It's an extension of PySerial Serial class.
    """
    def __init__(self, com_port, baud, data_max_count=1000):
        """
        Initialize Serial object.

        Parameters
        ----------
        com_port : str
            Name of the port to connect to.
        baud : int
            Baud rate which needs to be used during communication.
        data_max_count : int, default 1000
            Maximum length of array storing received data.
        """
        # initialize the parent class, which provides tools to facilitate the communication itself
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
        # try to start the communication, if not launched in mock mode
        try:
            if not self.mock:
                self.open()
        except SerialException:
            pass

        # if communication has started, not already receiving and not launched in mock mode
        if self.isOpen() and not self.receiving and not self.mock:
            # start the reception thread and set relevant flags
            self.receiving = True
            self.receiving_thread = threading.Thread(target=self.__receive, daemon=True)

            self.receiving_thread.start()
        # if not already receiving and launched in mock mode
        elif not self.receiving and self.mock: # For testing purposes only
            # start the thread which prepares mock signal data
            self.receiving = True
            self.receiving_thread = threading.Thread(target=self.__mock_receive, daemon=True)
            self.receiving_thread.start()
        else:
            self.__save_data(0)

    def __receive(self):
        """
        Method receiving the data inside of a separate thread.
        """
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
        For testing purposes only - mock data reception.
        Signal generated in this function will be a triangle wave.
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
        Decode the value passed as argument & cast it to int.

        Parameters
        ----------
        value : int
            Value to be decoded and cast to int.
        """
        try:
            return int(value.decode('Ascii').strip())
        except:
            return -100

    def __save_data(self, value):
        """
        Add the value to end of list of received data.
        If length of the list is bigger than specified on init - pop first element.

        Parameters
        ----------
        value : int
            Value that needs to be added to list of receivedf data.
        """
        self.received.append(value)

        # if length of the list is bigger than specified on init - pop first element
        if len(self.received) > self.data_max_count:
            self.received.pop(0)
    
    def stop_receiving(self):
        """
        Stop the thread which is receiving data over serial port.
        """
        if self.receiving:
            self.close()
            self.receiving = False
            self.receiving_thread.join()

    def get_received(self):
        """
        Return data received over serial port.

        Returns
        -------
        list of int
            Data received over serial port since the initialization.
        """
        return self.received

    def get_received_delta(self):
        """
        Return data received since last call of this method.

        Returns
        -------
        list of int
            Splice of received data - containing only values received since last call of this method.
        """
        points_count = self.count
        self.count = 0
        if points_count == 0:
            return []
        return self.received[-points_count:]

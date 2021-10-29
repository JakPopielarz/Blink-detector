import serial_utils

if __name__ == "__main__":
    comm = serial_utils.Serial("COM6", 9600)
    comm.receive() # it's blocking further execution

import serial_utils

if __name__ == "__main__":
    comm = serial_utils.Serial("COM5", 9600)
    comm.receive()

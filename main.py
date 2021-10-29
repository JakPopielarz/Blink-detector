import serial_utils
import time

if __name__ == "__main__":
    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()

    time.sleep(5)

    comm.stop_receiving()

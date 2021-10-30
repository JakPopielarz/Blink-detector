import time
import serial_utils
import plot_utils
import numpy

if __name__ == "__main__":
    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()

    time.sleep(5)

    data_range = numpy.linspace(0, 1024, num=comm.data_max_count)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), title="Signal strength", labels=['Sample #', 'Signal strength'])
    plotter.draw()

    time.sleep(5)
    plotter.update_data(y_data=comm.get_received())
    time.sleep(5)

    comm.stop_receiving()

import time
import numpy
import PySimpleGUI as sg

import serial_utils
import plot_utils
import receiver_window as rw


def example_receive():
    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()
    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024], \
        threshold=500)
    plotter.draw()

    while(True):
        plotter.update_data(y_data=comm.get_received())

    comm.stop_receiving()

def start():
    window = rw.create_window()

    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()
    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024], \
        threshold=500, interactive=False)
    plotter.draw()
    rw.add_plot(window, plotter.figure, "-CANVAS-")

    return window, plotter, comm

def stop(window, serial_communication):
    serial_communication.stop_receiving()
    window.close()


if __name__ == "__main__":
    # example_receive()
    window, plotter, comm = start()

    rw.run_window(window, plotter, comm)
    stop(window, comm)

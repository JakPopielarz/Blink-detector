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

if __name__ == "__main__":
    # example_receive()
    
    data_range = numpy.linspace(0, 1000, num=1000)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=[i for i in range(1000)], \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024], \
        interactive=False, threshold=500)
    plotter.draw()
    layout = [[sg.Text('Signal strength')],
        [sg.Canvas(key='-CANVAS-')],
        [sg.Button('Ok'), sg.Exit()]]
    window = rw.create_window(layout)
    rw.add_plot(window, plotter.figure, "-CANVAS-")
    rw.run_window(window)
    window.close()

import numpy

import detector_utils
import serial_utils
import plot_utils
import receiver_window as rw


def mock_receive():
    window = rw.create_window()

    comm = serial_utils.Serial("COM6", 9600)
    comm.mock = True
    comm.start_receiving()

    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024], \
        threshold=500)
    plotter.draw()
    rw.add_plot(window, plotter.figure, "-CANVAS-")
    
    rw.run_window(window, plotter, comm, mock=True)

    window.close()
    del window
    comm.stop_receiving()

def run_app():
    window, plotter, comm, det = start()

    rw.run_window(window, plotter, comm, det)
    stop(window, comm)

def start():
    window = rw.create_window()

    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()

    det = detector_utils.Detector(comm.get_received(), 200, 4.5, 0)

    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024])
    # assign the detector's output as plot data points - we won't need to explicitly
    # update plotter.signal_data anymore
    plotter.signal_data = det.signals
    plotter.draw()
    rw.add_plot(window, plotter.figure, "-CANVAS-")

    return window, plotter, comm, det

def stop(window, serial_communication):
    window.close()
    del window
    serial_communication.stop_receiving()


if __name__ == "__main__":
    # mock_receive()
    run_app()

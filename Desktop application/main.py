import numpy

import serial_utils
import plot_utils
import receiver_window as rw


def start_mock():
    """
    Start the whole application with all elements, but in mock mode.
    This means no attempts to connect to any serial port will be made.
    Instead the signal is generated artificially.
    """

    # create application window using PySimpleGui
    window = rw.create_window()

    # initiate serial communication in mock mode
    # initial arguments - COM6 serial port and 9600 baud rate won't be used,
    # but we need to initialize the object properly
    comm = serial_utils.Serial("COM6", 9600)
    comm.mock = True
    comm.start_receiving()

    # prepare range of x axis
    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    # initiate the plotting tool, along with setting title, labels and initial parameters
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1024], \
        threshold=500)
    # draw the plot for the first time - this allows us to load the plot / canvas element
    # of the app window fully
    plotter.draw()
    # add the plot to the window
    rw.add_plot(window, plotter.figure, "-CANVAS-")
    
    # start window operation - it contains a loop that's broken on window exit
    # rw.run_window(window, plotter, comm, det, mock=True)
    rw.run_window(window, plotter, comm, mock=True)

    # stop the window operation, delete it's object to make sure all threads are closed
    window.close()
    del window
    # stop the serial communication
    comm.stop_receiving()

def run_app():
    """
    Start the whole application with all elements.
    It will attempt to connect to the signal port specified during operation, as well as
    use the signal actually received from it.
    """
    # create & initialize all the elements needed - in order:
    # window, plotting tool, serial communication, signal analyzer
    window, plotter, comm = start()

    
    # start window operation - it contains a loop that's broken on window exit
    rw.run_window(window, plotter, comm)
    # stop the application if window was closed
    stop(window, comm)

def start():
    """
    Initialize all elements of the application.

    Returns
    -------
    PySimpleGui.Window
        Object of the window itself.
    plot_utils.Plotter
        Plotting tool object used to create signal plot.
    serial_utils.Serial
        Serial communication facilitator object used to receive data from USB device.
    detector_utils.Detector
        Signal analyzer object, which scans the signal received looking for peaks.
    """

    # create application window using PySimpleGui
    window = rw.create_window()

    # initiate serial communication with some initial arguments COM6 serial port and 9600 baud rate
    # the port chosen will probably be overriden once window starts operation, but we need to initialize
    # the object properly
    comm = serial_utils.Serial("COM6", 9600)
    comm.start_receiving()

    # prepare x axis data range
    data_range = numpy.linspace(0, comm.data_max_count, num=comm.data_max_count)
    # initiate the plotting tool, along with setting title, labels and initial parameters
    plotter = plot_utils.Plotter(x_data=data_range, y_data=comm.get_received(), \
        title="Signal strength", labels=['Sample #', 'Signal strength'], y_limits=[0, 1])
                # assign the detector's output as data points on the plot - we won't need to explicitly
                # update plotter.signal_data anymore
                # plotter.signal_data = det.signals
    # draw the plot for the first time - this allows us to load the plot / canvas element
    # of the app window fully
    plotter.draw()
    # add the plot to the window
    rw.add_plot(window, plotter.figure, "-CANVAS-")

    # return all the initalized objects
    return window, plotter, comm

def stop(window, serial_communication):
    """
    Ends all the threads created during app operation.

    Parameters
    ----------
    window : PySimpleGui.Window
        Object of the closed window - will need to properly end all threads connected to it.
    serial_communication : serial_utils.Serial
        Object facilitating the serial communication - needed to end the communication.
    """

    # stop the window operation, delete it's object to make sure all threads are closed
    window.close()
    del window
    # stop the serial communication
    serial_communication.stop_receiving()


if __name__ == "__main__":
    # Uncomment the line below (call to start_mock() function) to launch the application in test mode
    #  - it doesn't require the blink detector to be connected, but also doesn't offer full functionality
    #  - correct functioning of any and all features is not guaranteed
    # start_mock()

    # Uncomment the line below (call to run_app() function) to launch the application in "normal" mode
    #  - it requires the blink detector to be connected to work correctly
    run_app()

    # IMPORTANT : only one of the two calls should be left uncommented

import threading
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from  pynput.keyboard import Key, Listener
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController

matplotlib.use('TkAgg')

# variables used to handle the key/button press simulation
bind_keyboard = True
keyboard = KeyboardController()
key_bind = Key.enter

mouse = MouseController()
mouse_bind = Button.left

# theme of app window
sg.theme('DefaultNoMoreNagging')
# layout of configuration pane of elements - all user input fields
inputs_layout = [[sg.Text("COM port", size=10), sg.Input("COM6", key="-PORT_INPUT-", size=5, enable_events=True)],
    [sg.Text("Threshold", size=10), sg.Input("10", key="-THRESHOLD_INPUT-", size=5, enable_events=True)],
    [sg.Text("Key to press", size=10), sg.Input("Enter", key="-CURRENT_KEY-", size=5, enable_events=True, disabled=True), sg.Button("Change key", key="-CHANGE_KEY-", size=10)],
    [sg.Radio("Key", "BIND_RADIO", key="-KEY_BIND-", default=True, enable_events=True), sg.Radio("LMB", "BIND_RADIO", key="-LMB_BIND-", default=False, enable_events=True), 
        sg.Radio("RMB", "BIND_RADIO", key="-RMB_BIND-", default=False, enable_events=True)],
    [sg.Button("Calibrate", key="-CALIBRATE-"), sg.Button("Help", key="-HELP-")]]

# layout of the app window - left : configuration pane; right : plot
layout = [[sg.Frame("Configuration", inputs_layout, font='Helvetica 18'), sg.Canvas(key='-CANVAS-')],
    [sg.Button('Ok')]]

def draw_figure(canvas, figure):
    """
    Function that draws the plot in specified window element.

    Parameters
    ----------
    canvas : PySimpleGui.TKCanvas
        Element of window that's supposed to contain the plot.
    figure : matplotlib.Figure
        Object of figure with the plot that's supposed to be displayed in the window.
    
    Returns
    -------
    matplotlib.FigureCanvasTkAgg
        Figure handler compatible with TkInter.
    """
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def create_window():
    """
    Create the form and show it (without the plot).
    """
    return sg.Window('Blink detector configuration and signal reception', layout, finalize=True, element_justification='center', font='Helvetica 14')

def add_plot(window, figure, plot_key):
    """
    Add plot to the window.

    Parameters
    ----------
    window : PySimpleGui.Window
        Object of the application window.
    figure : matplotlib.Figure
        Object of figure with the plot that's supposed to be displayed in the window.
    plot_key : str
        Name of the element supposed to contain plot / figure.
    
    Returns
    -------
    matplotlib.FigureCanvasTkAgg
        Figure handler compatible with TkInter.
    """
    return draw_figure(window[plot_key].TKCanvas, figure)

def run_window(window, plotter=None, comm=None, det=None, mock=False):
    """
    Facilitate application window operations. Handle any changes in configuration, as well as orchestrate
    signal analysis.

    Parameters
    ----------
    window : PySimpleGui.Window
        Object of the application window.
    plotter : plot_utils.Plotter or None, default None
        Object of plotting tool.
    comm : serial_utils.Serial or None, default None
        Object of serial communication tool.
    det : detector_utils.Detector or None, default None
        Object of signal analysis tool.
    mock : bool, default False
        Flag indicating if the app was launched in testing mode.
    """

    global mouse_bind, bind_keyboard
    # load configuration specified by user on previous launch if available
    # any later changes to the configuration object will be automatically saved
    configuration = sg.UserSettings()
    configuration.load()
    apply_configuration(configuration, window, comm, det)

    # automatically launch signal analysis tool calibration on launch
    # calibrate(det, plotter, comm)

    # infinite loop, broken if window is closed
    while True:
        # check status of the window, wait max 100 ms for any change
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Ok':
            break
        # if plotting tool or serial communication tool wasn't initialized stop the app
        if plotter is None or comm is None:
            return
 
        # if signal analysis tool available: check signal for peaks
        if det is not None:
            check_receiving(comm, det)
            # only check new data points
            det.detect(len(comm.get_received_delta()))

        # no need to update the plotter y data, because it was inicialized as a reference to `received` array from object of Serial
        plotter.refresh_y_data()

        # # in case there would be a need to update the y data there are following methods provided:
        # plotter.update_data(y_data=comm.get_received())
        # plotter.append_y_data(comm.get_received_delta())

        # if serial port has been changed and not launched in test mode
        if event == "-PORT_INPUT-" and not mock:
            # change serial communication port
            port = values["-PORT_INPUT-"]
            comm.stop_receiving()
            comm.port = port
            comm.start_receiving()
            # make sure to save it in configuration
            configuration['-port-'] = port
        # if serial port has been changed and launched in test mode
        elif event == "-PORT_INPUT-":
            # change only in the configuration
            port = values["-PORT_INPUT-"]
            configuration['-port-'] = port
        # if the `change key` button has been pressed
        elif event == "-CHANGE_KEY-":
            # launch the rebinding function
            handle_key_bind(window, "-CURRENT_KEY-")
            # make sure to save it in configuration
            configuration['-key-'] = str(window["-CURRENT_KEY-"].get())
        # if the `use LMB` radio button has been pressed
        elif event == "-LMB_BIND-":
            # rebind to the left mouse button
            bind_keyboard = False
            mouse_bind = Button.left
            # make sure to save it in configuration
            configuration['-bind-'] = 'LMB'
        # if the `use RMB` radio button has been pressed
        elif event == "-RMB_BIND-":
            # rebind to the right mouse button
            bind_keyboard = False
            mouse_bind = Button.right
            # make sure to save it in configuration
            configuration['-bind-'] = 'RMB'
        # if the `use Keyboard key` radio button has been pressed
        elif event == "-KEY_BIND-":
            # rebind to keyboard - key from the key display element will be used
            bind_keyboard = True
            # make sure to save it in configuration
            configuration['-bind-'] = 'KEY'
        # if the `calibrate` button has been pressed
        elif event == "-CALIBRATE-":
            # launch calibration function
            calibrate(det, plotter, comm)
        # if the `help` button has been pressed
        elif event == "-HELP-":
            display_help()
        # if the threshold value has been changed
        elif event == "-THRESHOLD_INPUT-":
            # apply the change to the singal analysis tool also
            handle_threshold(values['-THRESHOLD_INPUT-'], window, det)
            # make sure to save it in configuration
            configuration['-threshold-'] = values['-THRESHOLD_INPUT-']

def apply_configuration(configuration, window, comm, det):
    """
    Apply the configuration specified by user on previous launch, if avaliable.
    Update the relevant objects and window elements.

    Parameters
    ----------
    configuration : PySimpleGui.UserConfiguration
        Object containing loaded configuration data.
    window : PySimpleGui.Window
        Object of the application window.
    comm : serial_utils.Serial or None, default None
        Object of serial communication tool.
    det : detector_utils.Detector or None, default None
        Object of signal analysis tool.
    """
    global mouse_bind, bind_keyboard
    # apply serial port name if available
    if configuration['-port-']:
        port = configuration['-port-']
        window['-PORT_INPUT-'].update(port)
        if comm:
            comm.stop_receiving()
            comm.port = port
            comm.start_receiving()
    # update key bind display element
    if configuration['-key-']:
        window['-CURRENT_KEY-'].update(configuration['-key-'])
    # select key or button simulation
    if configuration['-bind-'] == 'LMB':
        bind_keyboard = False
        mouse_bind = Button.left
        window['-LMB_BIND-'].update(True)
        window['-RMB_BIND-'].update(False)
        window['-KEY_BIND-'].update(False)
    elif configuration['-bind-'] == 'RMB':
        bind_keyboard = False
        mouse_bind = Button.right
        window['-LMB_BIND-'].update(False)
        window['-RMB_BIND-'].update(True)
        window['-KEY_BIND-'].update(False)
    elif configuration['-bind-'] == 'KEY':
        # if a key was bound - ask user to bind new key
        handle_key_bind(window, "-CURRENT_KEY-")
        bind_keyboard = True
        window['-LMB_BIND-'].update(False)
        window['-RMB_BIND-'].update(False)
        window['-KEY_BIND-'].update(True)
    # apply threshold (standard deviation multiply) if available
    if configuration['-threshold-']:
        window['-THRESHOLD_INPUT-'].update(configuration['-threshold-'])
        det.threshold = float(configuration['-threshold-'])
    
    # if this is the first launch of the application - automatically display the help text
    if not configuration['-first-']:
        display_help()

    # indicate that the application has been launched, so the help text won't be displayed on next launch
    configuration['-first-'] = "False"

def calibrate(det, plotter, comm):
    """
    Calibrate the signal analysis tool.

    Parameters
    ----------
    det : detector_utils.Detector
        Object of signal analysis tool.
    plotter : plot_utils.Plotter
        Object of plotting tool.
    comm : serial_utils.Serial
        Object of serial communication tool.
    """
    # mark that the calibration has started
    det.calibrating = True
    # launch the calibration thread
    # the coma in args tuple for threading.Thread is necessary for it to be treated as tuple, not a string, and thus properly passing the argument to target method
    calibration_thread = threading.Thread(target=det.gather_calibration_data, args=(comm.get_received_delta,))
    calibration_thread.start()

    # display a pop up with info about the calibration for 10 seconds
    sg.Popup("Please wait for the calibration to complete.\nPlease don't try to do anything in particular, just be yourself and enjoy the calibration period. It shouldn't take more than 10 seconds, so not much more to go!", auto_close=True, auto_close_duration=10, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)

    # after the pop up closed stop the thread
    det.calibrating = False
    calibration_thread.join()
    
    # calculate new values
    det.calibrate()

    # make sure to update the threshold plot accordingly
    update_plot_threshold(det.border, plotter)

def update_plot_threshold(new_val, plotter):
    """
    Update the threshold plot with new value.

    Parameters
    ----------
    new_val : int
        New Y axis value of the threshold
    plotter : plot_utils.Plotter
        Object of plotting tool.
    """
    plotter.update_threshold(new_val)

def check_receiving(comm, det):
    """
    Make sure there were no errors in serial communication. If everything's going smoothly check if any blinks were detected.

    Parameters
    ----------
    comm : serial_utils.Serial
        Object of serial communication tool.
    det : detector_utils.Detector
        Object of signal analysis tool.
    """
    if comm is None:
        return
    elif comm.error_in_receiving:
        comm.stop_receiving()
        comm.error_in_receiving = False
    elif not comm.receiving:
        comm.start_receiving()
    else:
        check_for_blink(comm, det)

def check_for_blink(comm, det):
    """
    Check if any blinks were detected. If so - simulate the press of set button / key.

    Parameters
    ----------
    comm : serial_utils.Serial
        Object of serial communication tool.
    det : detector_utils.Detector
        Object of signal analysis tool.
    """
    if not comm.triggered and det.signals[-1] > 600:
        comm.triggered = True
        if bind_keyboard:
            keyboard.press(key_bind)
            keyboard.release(key_bind)
        else:
            mouse.press(mouse_bind)
            mouse.release(mouse_bind)
    elif comm.triggered and det.signals[-1] <= 600:
        comm.triggered = False

def handle_key_bind(window, text_key):
    """
    Handle the ``change key`` button press. Displays a pop-up window with a key press listener (looking for new bind).

    Parameters
    ----------
    window : PySimpleGui.Window
        Object of the application window.
    text_key : str
        Name of the element displaying currently bound key.
    """
    def __rebind(bind):
        """
        Inner function used in the listener thread.

        Parameters
        ----------
        bind : pynput.Key
            Object of the key that was pressed.
        """
        # set the new key bind
        global key_bind
        key_bind = bind
        # also in the display element in window
        text_val = str(bind)
        if text_val.startswith('Key'):
            text_val = text_val[4:]
        else:
            text_val = text_val[1:-1]
        window[text_key].update(text_val)

    # start key listener thread
    key_listener = Listener(on_release=__rebind)
    key_listener.start()
    # display key bind pop up
    sg.Popup("Press the button you want to be pressed", keep_on_top=True, any_key_closes=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
    # stop the listener thread (after pop up was clossed - on any key press)
    key_listener.stop()

def display_help():
    """
    Display a pop-up window with text specified in help_text variable.
    """

    help_text = """Hi!
    On the right side of the main window you can see the plot of current signal, threshold and detection.
    The blue, wiggly line is signal received from the device.
    The red, straight line is the current detection border - calculated as threshold * standard deviation + mean of the received signal.
    The orange line depicts the detections - if it raises to the top a blink has been detected.

    On the left side of the main window you can see the configuration pane and in it some fields:
    - COM port : the serial communication port through which the communication happens. Make sure to select the one that your device is connected into.
    - Threshold : the number of standart deviations from the mean above which the blink will be detected. Marked on the plot with a red line (value = threshold * standard deviation + mean). IMPORTANT: Changing this doesn't take effect untill calibration!
    - Key to press : just displays the current keybind, which can be changed using the "Change key" button. During changing the bind blink detection will be suspended untill a key is pressed (and thus key bound).
    - Key / LMB / RMB : radio buttons, which specify wheter the bound key, or according (left/right) mouse button will be pressed on blink detection.
    - Calibrate : button starting the calibration process. It takes around 10 seconds, so get comfortable and relax.
    - Help button : displays this window.
    """
    sg.Popup(help_text, keep_on_top=True)

def handle_threshold(new_val, window, det):
    """
    Handle a change made in Threshold input window.

    Parameters
    ----------
    new_val : str
        Value entered in the input window.
    window : PySimpleGui.Window
        Object of the application window.
    det : detector_utils.Detector
        Object of singal analyzer.
    """

    # parse the new value - if it's empty set it to 0
    if new_val == '':
        new_val = '0'
    try:
        new_val = float(new_val)
    except ValueError:
        # if an invalid (non-numerical) value was entered clear the input field
        new_val = 0
        window['-THRESHOLD_INPUT-'].Update('')
    
    # update the threshold also in the signal analyzer
    det.threshold = new_val

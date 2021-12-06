# from matplotlib.ticker import NullFormatter  # useful for `logit` scale
# import matplotlib.pyplot as plt
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
from  pynput.keyboard import Key, Listener
from pynput.keyboard import Controller as KeyboardController
from pynput.mouse import Button
from pynput.mouse import Controller as MouseController
matplotlib.use('TkAgg')


bind_keyboard = True
keyboard = KeyboardController()
key_bind = Key.enter

mouse = MouseController()
mouse_bind = Button.left

sg.theme('DefaultNoMoreNagging')
inputs_layout = [[sg.Text("COM port", size=15), sg.Input("COM6", key="-PORT_INPUT-", size=5, enable_events=True)],
    [sg.Text("Threshold", size=15), sg.Input(500, key="-THRESHOLD_INPUT-", size=5, enable_events=True)],
    [sg.Radio("Single blink to activate", "ACTIVATION_RADIO", key="-1_BLINK_ACTIVATE-", default=True, disabled=True)],
    [sg.Radio("Double blink to activate", "ACTIVATION_RADIO", key="-2_BLINK_ACTIVATE-", default=False, disabled=True)],
    [sg.Text("Key to press", size=10), sg.Input("Enter", key="-CURRENT_KEY-", size=5, enable_events=True, disabled=True), sg.Button("Change key", key="-CHANGE_KEY-", size=10)],
    [sg.Radio("Key", "BIND_RADIO", key="-KEY_BIND-", default=True, enable_events=True), sg.Radio("LMB", "BIND_RADIO", key="-LMB_BIND-", default=False, enable_events=True), 
        sg.Radio("RMB", "BIND_RADIO", key="-RMB_BIND-", default=False, enable_events=True)]]

layout = [[sg.Frame("Configuration", inputs_layout, font='Helvetica 18'), sg.Canvas(key='-CANVAS-')],
    [sg.Button('Ok')]]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# create the form and show it without the plot
def create_window():
    return sg.Window('Blink detector configuration and signal reception', layout, finalize=True, element_justification='center', font='Helvetica 14')


# add the plot to the window
def add_plot(window, figure, plot_key):
    return draw_figure(window[plot_key].TKCanvas, figure)

def run_window(window, plotter=None, comm=None, mock=False):
    global mouse_bind, bind_keyboard
    configuration = sg.UserSettings()
    configuration.load()
    apply_configuration(configuration, window, plotter, comm)

    while True:
        event, values = window.read(timeout=100)
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Ok':
            break
        if plotter is None or comm is None:
            return

        # no need to update the plotter y data, because it was inicialized as a reference to `received` array from object of Serial
        plotter.refresh_y_data()

        # in case there would be a need to update the y data there are following methods provided:
        # plotter.update_data(y_data=comm.get_received())
        # plotter.append_y_data(comm.get_received_delta())

        threshold_value = int(values['-THRESHOLD_INPUT-'])
        if event == '-THRESHOLD_INPUT-':
            threshold_value = handle_threshold(values['-THRESHOLD_INPUT-'], plotter, window)
            configuration['-threshold-'] = threshold_value

        check_receiving(comm, window, threshold_value)

        if event == "-PORT_INPUT-" and not mock:
            port = values["-PORT_INPUT-"]
            comm.stop_receiving()
            comm.port = port
            comm.start_receiving()
            configuration['-port-'] = port
        elif event == "-PORT_INPUT-":
            port = values["-PORT_INPUT-"]
            configuration['-port-'] = port
        elif event == "-CHANGE_KEY-":
            handle_key_bind(window, "-CURRENT_KEY-")
            configuration['-key-'] = str(window["-CURRENT_KEY-"].get())
        elif event == "-LMB_BIND-":
            bind_keyboard = False
            mouse_bind = Button.left
            configuration['-bind-'] = 'LMB'
        elif event == "-RMB_BIND-":
            bind_keyboard = False
            mouse_bind = Button.right
            configuration['-bind-'] = 'RMB'
        elif event == "-KEY_BIND-":
            bind_keyboard = True
            configuration['-bind-'] = 'KEY'

def apply_configuration(configuration, window, plotter, comm):
    global mouse_bind, bind_keyboard
    if configuration['-threshold-']:
        threshold_value = configuration['-threshold-']
        window['-THRESHOLD_INPUT-'].update(threshold_value)
        handle_threshold(threshold_value, plotter, window)
    if configuration['-port-']:
        port = configuration['-port-']
        window['-PORT_INPUT-'].update(port)
        if comm:
            comm.stop_receiving()
            comm.port = port
            comm.start_receiving()
    if configuration['-key-']:
        window['-CURRENT_KEY-'].update(configuration['-key-'])
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
        handle_key_bind(window, "-CURRENT_KEY-")
        bind_keyboard = True
        window['-LMB_BIND-'].update(False)
        window['-RMB_BIND-'].update(False)
        window['-KEY_BIND-'].update(True)

def check_receiving(comm, window, threshold_value):
    if comm is None:
        return
    elif comm.error_in_receiving:
        block_inputs(window)
        comm.stop_receiving()
        comm.error_in_receiving = False
    elif not comm.receiving:
        block_inputs(window)
        comm.start_receiving()
    else:
        check_for_blink(comm, threshold_value)
        unblock_inputs(window)

def block_inputs(window):
    window['-THRESHOLD_INPUT-'].update(disabled=True)
    window['-1_BLINK_ACTIVATE-'].update(disabled=True)
    window['-2_BLINK_ACTIVATE-'].update(disabled=True)
    window['-CHANGE_KEY-'].update(disabled=True)

def unblock_inputs(window):
    window['-THRESHOLD_INPUT-'].update(disabled=False)
    # window['-1_BLINK_ACTIVATE-'].update(disabled=False)
    # window['-2_BLINK_ACTIVATE-'].update(disabled=False)
    window['-CHANGE_KEY-'].update(disabled=False)

def check_for_blink(comm, threshold_value):
    sensor_data = comm.get_received()
    if not comm.triggered and sensor_data[-1] >= threshold_value:
        comm.triggered = True
        if bind_keyboard:
            keyboard.press(key_bind)
            keyboard.release(key_bind)
        else:
            mouse.press(mouse_bind)
            mouse.release(mouse_bind)
    elif comm.triggered and sensor_data[-1] < threshold_value:
        comm.triggered = False

def handle_threshold(new_val, plotter, window):
    if new_val == '':
        new_val = '0'
    try:
        new_val = int(new_val)
    except ValueError:
        new_val = 0
        window['-THRESHOLD_INPUT-'].Update('')
    plotter.update_threshold(new_val)
    return new_val

def handle_key_bind(window, text_key):
    def __rebind(bind):
        global key_bind
        key_bind = bind
        text_val = str(bind)
        if text_val.startswith('Key'):
            text_val = text_val[4:]
        else:
            text_val = text_val[1:-1]
        window[text_key].update(text_val)

    # block_inputs(window)
    key_listener = Listener(on_release=__rebind)
    key_listener.start()
    sg.Popup("Press the button you want to be pressed", keep_on_top=True, any_key_closes=True, button_type=sg.POPUP_BUTTONS_NO_BUTTONS)
    key_listener.stop()


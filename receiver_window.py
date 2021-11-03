# from matplotlib.ticker import NullFormatter  # useful for `logit` scale
# import matplotlib.pyplot as plt
from logging import disable
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('TkAgg')


sg.theme('DefaultNoMoreNagging')
inputs_layout = [[sg.Text("COM port", size=15), sg.Input('COM6', key="-PORT_INPUT-", size=5, enable_events=True)],
    [sg.Text("Threshold", size=15), sg.Input(500, key="-THRESHOLD_INPUT-", size=5, enable_events=True)],
    [sg.Radio("Single blink to activate", "ACTIVATION_RADIO", key="-1_BLINK_ACTIVATE-", default=True)],
    [sg.Radio("Double blink to activate", "ACTIVATION_RADIO", key="-2_BLINK_ACTIVATE-", default=False)],
    [sg.Text("Key to press", size=15), sg.Button("Enter", key="-KEY_BIND-", size=5)]]

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

def run_window(window, plotter=None, comm=None):
    while True:
        if plotter is not None and comm is not None:
            plotter.update_data(y_data=comm.get_received())
        event, values = window.read(timeout=100)
        
        check_receiving(comm, window)

        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Ok':
            break
        elif event == '-THRESHOLD_INPUT-' and plotter is not None:
            handle_threshold(values['-THRESHOLD_INPUT-'], plotter, window)
        elif event == "-PORT_INPUT-":
            comm.port = values["-PORT_INPUT-"]

def check_receiving(comm, window):
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
        unblock_inputs(window)

def block_inputs(window):
    window['-THRESHOLD_INPUT-'].update(disabled=True)
    window['-1_BLINK_ACTIVATE-'].update(disabled=True)
    window['-2_BLINK_ACTIVATE-'].update(disabled=True)
    window['-KEY_BIND-'].update(disabled=True)

def unblock_inputs(window):
    window['-THRESHOLD_INPUT-'].update(disabled=False)
    window['-1_BLINK_ACTIVATE-'].update(disabled=False)
    window['-2_BLINK_ACTIVATE-'].update(disabled=False)
    window['-KEY_BIND-'].update(disabled=False)

def handle_threshold(new_val, plotter, window):
    if new_val == '':
        new_val = '0'
    try:
        new_val = int(new_val)
    except ValueError:
        new_val = 0
        window['-THRESHOLD_INPUT-'].Update('')
    plotter.update_threshold(new_val)


if __name__ == "__main__":
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    window = create_window()
    add_plot(window, fig, "-CANVAS-")
    run_window(window)
    window.close()

# from matplotlib.ticker import NullFormatter  # useful for `logit` scale
# import matplotlib.pyplot as plt
import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('TkAgg')

inputs_layout = [[sg.Text("Threshold", size=15), sg.Input(key="-THRESHOLD_INPUT-", size=5)],
    [sg.Checkbox("Single blink to activate", key="-1_BLINK_ACTIVATE-")],
    [sg.Checkbox("Double blink to activate", key="-2_BLINK_ACTIVATE-")],
    [sg.Text("Key to press", size=15), sg.Input(size=5)]]

layout = [[sg.Column(inputs_layout), sg.Canvas(key='-CANVAS-')],
    [sg.Button('Ok')]]

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# create the form and show it without the plot
def create_window():
    sg.theme('DefaultNoMoreNagging')
    return sg.Window('Blink detector configuration and signal reception', layout, finalize=True, element_justification='center', font='Helvetica 18')


# add the plot to the window
def add_plot(window, figure, plot_key):
    return draw_figure(window[plot_key].TKCanvas, figure)

def run_window(window, plotter=None, comm=None):
    while True:
        if plotter is not None and comm is not None:
            plotter.update_data(y_data=comm.get_received())
        event, values = window.read(timeout=100)  
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Ok':
            break

if __name__ == "__main__":
    fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

    window = create_window()
    add_plot(window, fig, "-CANVAS-")
    run_window(window)
    window.close()

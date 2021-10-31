# from matplotlib.ticker import NullFormatter  # useful for `logit` scale
# import matplotlib.pyplot as plt
# import numpy as np
import matplotlib
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import PySimpleGUI as sg
matplotlib.use('TkAgg')

def draw_figure(canvas, figure):
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

# create the form and show it without the plot
def create_window(layout):
    return sg.Window('Blink detector configuration and signal reception', layout, finalize=True, element_justification='center', font='Helvetica 18')


# add the plot to the window
def add_plot(window, figure, plot_key):
    return draw_figure(window[plot_key].TKCanvas, figure)

def run_window(window):
    while True:
        event, values = window.read()    
        if event == sg.WIN_CLOSED or event == 'Exit' or event == 'Ok':
            break    

# if __name__ == "__main__":
#     fig = matplotlib.figure.Figure(figsize=(5, 4), dpi=100)
#     t = np.arange(0, 3, .01)
#     fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))

#     layout = [[sg.Text('Signal strength')],
#           [sg.Canvas(key='-CANVAS-')],
#           [sg.Button('Ok'), sg.Exit()]]
#     window = create_window(layout)
#     add_plot(window, fig, "-CANVAS-")
#     run_window(window)
#     window.close()

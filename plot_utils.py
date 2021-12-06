import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, x_data=None, y_data=None, interactive=False, title='', labels=[], x_limits=[], y_limits=[], max_data_points=1000):
        self.x_data = x_data
        self.y_data = y_data
        self.figure = None
        self.line_plot = None
        while len(labels) < 2:
            labels.append("")
        self.text = {'title': title, 'x_label': labels[0], 'y_label': labels[1]}
        self.limits = {'x': x_limits, 'y': y_limits}
        if interactive:
            plt.ion()
        else:
            plt.ioff()
        self.max_data_points = max_data_points

        self.signal_data = [0] * max_data_points
        self.signal_plot = None

    def draw(self):
        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)
        ax.set_title(self.text['title'])
        ax.set_xlabel(self.text['x_label'])
        if len(self.limits['x']) == 2:
            ax.set_xlim(self.limits['x'])
        ax.set_ylabel(self.text['y_label'])
        if len(self.limits['y']) == 2:
            ax.set_ylim(self.limits['y'])
        self.line_plot, = ax.plot(self.y_data)

        self.signal_plot, = ax.plot(self.signal_data)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def update_data(self, x_data=None, y_data=None):
        if (x_data is None and y_data is None) or self.line_plot is None:
            return

        if y_data is not None:
            self.y_data = y_data
            self.line_plot.set_ydata(y_data)
        if x_data is not None:
            self.x_data = x_data
            self.line_plot.set_xdata(x_data)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def append_y_data(self, data_to_append):
        if self.line_plot is None:
            return

        print(self.y_data, data_to_append)

        self.y_data += data_to_append
        while len(self.y_data) > self.max_data_points:
            self.y_data.pop(0)

        print(self.y_data, len(self.y_data))
        
        self.line_plot.set_ydata(self.y_data)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def refresh_y_data(self):
        if self.line_plot is None:
            return
        self.line_plot.set_ydata(self.y_data)
        self.signal_plot.set_ydata(self.signal_data)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, x_data=None, y_data=None, interactive=True, title='', labels=[], x_limits=[], y_limits=[], threshold=None):
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
        self.threshold = threshold
        self.threshold_line = None

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

        if self.threshold is not None:
            self.threshold_line, = ax.plot([0, max(self.x_data)], [self.threshold, self.threshold], color='r')

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def update_data(self, x_data=None, y_data=None):
        if (x_data is None and y_data is None) or self.line_plot == None:
            return

        if y_data is not None:
            self.line_plot.set_ydata(y_data)
        if x_data is not None:
            self.line_plot.set_xdata(x_data)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def update_threshold(self, threshold):
        self.threshold = threshold
        self.threshold_line.set_ydata([threshold, threshold])
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
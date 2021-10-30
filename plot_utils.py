import matplotlib.pyplot as plt

class Plotter:
    def __init__(self, x_data=None, y_data=None, interactive=True, title='', labels=[]):
        self.x_data = x_data
        self.y_data = y_data
        self.figure = None
        self.line_plot = None
        while len(labels) < 2:
            labels.append("")
        self.text = {'title': title, 'x_label': labels[0], 'y_label': labels[1]}
        if interactive:
            plt.ion()
        else:
            plt.ioff()

    def draw(self):
        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)
        ax.set_title(self.text['title'])
        ax.set_xlabel(self.text['x_label'])
        ax.set_ylabel(self.text['y_label'])
        self.line_plot, = ax.plot(self.y_data, 'r-')
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

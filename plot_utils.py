import matplotlib.pyplot as plt

class Plotter:
    """
    Plotting tool class. It can be used to draw a figure containing 3 line plots - signal, detection results and threshold.
    """
    def __init__(self, x_data=None, y_data=None, interactive=False, title='', labels=[], x_limits=[], y_limits=[], max_data_points=1000, threshold=0):
        """
        Initialize Plotter object.

        Parameters
        ----------
        x_data : list of int, default None
            Array of X axis values of data points to be plotted (signal data).
        y_data : list of int, default None
            Array of Y axis values of data points to be plotted (signal data).
        interactive : bool, default False
            Flag specifying the pyplot environment. Should be left at false.
        title : str, default ''
            Title of the figure.
        labels : list of str, default []
            List containing axis labels - first element will be used as X axis label, second as Y axis label.
        x_limits : list of int, default []
            List containing X axis limits - first element will be used as min, second as max.
        y_limits : list of int, default []
            List containing Y axis limits - first element will be used as min, second as max.
        max_data_points : int, default 1000
            Max number of data points. All plots on figure must have the same max data points value.
        threshold : int or None
            Value at which the threshold line will be drawn. If the value will be None no threshold will be drawn.
        """
        self.y = y_data
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

        self.threshold = threshold
        self.threshold_line = None

        self.signal_data = [0] * max_data_points
        self.signal_plot = None

    def draw(self):
        """
        Draw the figure containing relevant plots.
        """

        # prepare figure and axes
        self.figure = plt.figure()
        ax = self.figure.add_subplot(111)
        # set title, labels and limits
        ax.set_title(self.text['title'])
        ax.set_xlabel(self.text['x_label'])
        if len(self.limits['x']) == 2:
            ax.set_xlim(self.limits['x'])
        ax.set_ylabel(self.text['y_label'])
        if len(self.limits['y']) == 2:
            ax.set_ylim(self.limits['y'])
        # plot the signal data
        self.line_plot, = ax.plot(self.y_data)

        # plot threshold line (flat) if relevant
        if self.threshold is not None:
            self.threshold_line, = ax.plot([0, max(self.x_data)], [self.threshold, self.threshold], color='r')

        # plot the detection results
        self.signal_plot, = ax.plot(self.signal_data)

        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def update_data(self, x_data=None, y_data=None):
        """
        Update signal data plot on the figure.

        Parameters
        ----------
        x_data : list of int or None
            List containing new X values of all data points. If None, no change will be applied.
        y_data : list of int or None
            List containing new Y values of all data points. If None, no change will be applied.
        """
        # check if there's anything to update
        if (x_data is None and y_data is None) or self.line_plot is None:
            return

        # update relevant data
        if y_data is not None:
            self.y_data = y_data
            self.line_plot.set_ydata(y_data)
        if x_data is not None:
            self.x_data = x_data
            self.line_plot.set_xdata(x_data)
        # redraw the figure to apply changes visually
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def append_y_data(self, data_to_append):
        """
        Add new values to the list of Y values of signal data points.

        Parameters
        ----------
        data_to_append : list of int
            List of values that need to be added to signal data points list.
        """
        if self.line_plot is None:
            return

        # add the data and make sure list will still have the correct length
        self.y_data += data_to_append
        while len(self.y_data) > self.max_data_points:
            self.y_data.pop(0)
        
        # apply the changes to the plot
        self.line_plot.set_ydata(self.y_data)
        # redraw the figure to apply changes visually
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
    
    def refresh_y_data(self):
        """
        Redraw the signal data and detection results plot.
        """
        if self.line_plot is None:
            return
        self.line_plot.set_ydata(self.y_data)
        self.signal_plot.set_ydata(self.signal_data)
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()

    def update_threshold(self, threshold):
        """
        Update value of drawn threshold plot.

        Parameters
        ----------

        threshold : int
            New Y value of threshold line.
        """

        # apply the changes
        self.threshold = threshold
        self.threshold_line.set_ydata([threshold, threshold])
        # redraw the figure to apply changes visually
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
